"""
IndicatorIndicatorlocationdata -----
1)
Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title

d. denominatro
v. enumaror
c. calc

2)
Indicator ID                Reportable.id
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Reported Total                  IndicatorLocationData.disaggregation['()']['c']



Country                         CoreCountry.name
Partner                         PartnerPartner.title
PD                              UnicefProgrammedocument.reference_number
Indicator Target                Reportable.target
Indicator Baseline              Reportable.baseline
Title of Indicator              Reportable.blueprint.title
Calculation across periods      'sum' 'max'...
Calculation across locations    'sum' 'max'....
Means of Verification           Reportable.means_of_verification
Indicator Results level         ???
Indicator Location Name         IndicatorLocationData.location.name
Indicator Location Geo          IndicatorLocationData.location.point
Admin level of location         IndicatorLocationData.location.type.admin_level
Frequency                       IndicatorReport.frequency (Reportable, ProgrammeDocument ??)
Overall Status                  ProgressReport.review_overall_status
Narrative Assessment            IndicatorReport.narrative_assessment
Due date                        IndicatorReport.due_date
Submission date                 IndicatorReport.submission_date
Project activity                (cannot find this field maybe PartnerActivity?)

Totalbudget(ideally at most granular level tied to activity / result)
Utilised budget(same conditions as above)
Report  #
"""


from django.db import transaction
from django.utils import timezone

from redis.exceptions import LockError

from etools_datamart.apps.etl.exceptions import MaxRecordsException, RequiredIsMissing, RequiredIsRunning
from etools_datamart.apps.etl.loader import BaseLoader, EtlResult, logger, RUN_UNKNOWN
from etools_datamart.sentry import process_exception


class PrpBaseLoader(BaseLoader):

    def get_queryset(self):
        if self.config.queryset:
            ret = self.config.queryset
        elif self.config.source:
            ret = self.config.source.objects.all()
        else:  # pragma: no cover
            raise ValueError("Option must define 'queryset' or 'source' attribute")

        return ret

    def filter_queryset(self, qs):
        use_delta = self.context['only_delta'] and not self.context['is_empty']
        if self.config.filters:
            qs = qs.filter(**self.config.filters)
        if use_delta and (self.config.last_modify_field and self.last_run):
            logger.debug(f"Loader {self}: use deltas")
            qs = qs.filter(**{f"{self.config.last_modify_field}__gte": self.last_run})
        return qs

    def load(self, *, verbosity=0, stdout=None,
             ignore_dependencies=False, max_records=None,
             only_delta=True, run_type=RUN_UNKNOWN, **kwargs):
        self.on_start(run_type)
        self.results = EtlResult()
        logger.debug(f"Running loader {self}")
        lock = self.lock()
        truncate = self.config.truncate
        try:
            if lock:  # pragma: no branch
                if not ignore_dependencies:
                    for requirement in self.config.depends:
                        if requirement.loader.is_running():
                            raise RequiredIsRunning(requirement)
                        if requirement.loader.need_refresh(self):
                            raise RequiredIsMissing(requirement)
                        else:
                            logger.info(f"Loader {requirement} is uptodate")
                self.mapping = {}
                mart_fields = self.model._meta.concrete_fields
                for field in mart_fields:
                    if field.name not in ['source_id', 'id', 'last_modify_date']:
                        self.mapping[field.name] = field.name
                if self.config.mapping:  # pragma: no branch
                    self.mapping.update(self.config.mapping)
                self.update_context(today=timezone.now(),
                                    max_records=max_records,
                                    verbosity=verbosity,
                                    records=0,
                                    only_delta=only_delta,
                                    is_empty=not self.model.objects.exists(),
                                    stdout=stdout)
                sid = transaction.savepoint()
                try:
                    self.results.context = self.context
                    self.fields_to_compare = [f for f in self.mapping.keys() if f not in ["seen"]]
                    if truncate:
                        self.model.objects.truncate()
                    qs = self.filter_queryset(self.get_queryset())
                    for record in qs.all():
                        filters = self.config.key(self, record)
                        values = self.get_values(record)
                        op = self.process_record(filters, values)
                        self.increment_counter(op)

                    if stdout and verbosity > 0:
                        stdout.write("\n")
                    # deleted = self.model.objects.exclude(seen=today).delete()[0]
                    # self.results.deleted = deleted
                except MaxRecordsException:
                    pass
                except Exception:
                    transaction.savepoint_rollback(sid)
                    raise
            else:
                logger.info(f"Unable to get lock for {self}")

        except (RequiredIsMissing, RequiredIsRunning) as e:
            self.on_end(error=e, retry=True)
            raise
        except BaseException as e:
            self.on_end(e)
            process_exception(e)
            raise
        else:
            self.on_end(None)
        finally:
            if lock:  # pragma: no branch
                try:
                    lock.release()
                except LockError as e:  # pragma: no cover
                    logger.warning(e)

        return self.results
