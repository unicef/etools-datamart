# -*- coding: utf-8 -*-
import logging

from django.db import connections
from django.db.models import QuerySet
from django.db.models.query import ModelIterable, RelatedPopulator

logger = logging.getLogger(__name__)


class TenantRelatedPopulator(RelatedPopulator):
    """
    RelatedPopulator is used for select_related() object instantiation.

    The idea is that each select_related() model will be populated by a
    different RelatedPopulator instance. The RelatedPopulator instances get
    klass_info and select (computed in SQLCompiler) plus the used db as
    input for initialization. That data is used to compute which columns
    to use, how to instantiate the model, and how to populate the links
    between the objects.

    The actual creation of the objects is done in populate() method. This
    method gets row and from_obj as input and populates the select_related()
    model instance.
    """

    # def __init__(self, klass_info, select, db):
    #     self.db = db
    #     select_fields = klass_info['select_fields']
    #     from_parent = klass_info['from_parent']
    #     if not from_parent:
    #         self.cols_start = select_fields[0]
    #         self.cols_end = select_fields[-1] + 1
    #         self.init_list = [
    #             f[0].target.attname for f in select[self.cols_start:self.cols_end]
    #         ]
    #         self.reorder_for_init = None
    #     else:
    #         attname_indexes = {select[idx][0].target.attname: idx for idx in select_fields}
    #         model_init_attnames = (f.attname for f in klass_info['model']._meta.concrete_fields)
    #         self.init_list = [attname for attname in model_init_attnames if attname in attname_indexes]
    #         self.reorder_for_init = operator.itemgetter(*[attname_indexes[attname] for attname in self.init_list])
    #
    #     self.model_cls = klass_info['model']
    #     self.pk_idx = self.init_list.index(self.model_cls._meta.pk.attname)
    #     self.related_populators = get_related_populators(klass_info, select, self.db)
    #     self.local_setter = klass_info['local_setter']
    #     self.remote_setter = klass_info['remote_setter']

    def populate(self, row, from_obj):
        if self.reorder_for_init:
            obj_data = self.reorder_for_init(row)
        else:
            obj_data = row[self.cols_start:self.cols_end]
        if obj_data[self.pk_idx] is None:
            obj = None
        else:
            init_list = self.init_list.copy()
            if 'schema' in init_list:
                init_list.remove('schema')
            obj = self.model_cls.from_db(self.db, init_list, obj_data)
            if self.related_populators:
                for rel_iter in self.related_populators:
                    rel_iter.populate(row, obj)
        self.local_setter(from_obj, obj)
        if obj is not None:
            self.remote_setter(obj, from_obj)


# need to be overridden on because TenantRelatedPopulator()
def get_related_populators(klass_info, select, db):
    iterators = []
    related_klass_infos = klass_info.get('related_klass_infos', [])
    for rel_klass_info in related_klass_infos:
        rel_cls = TenantRelatedPopulator(rel_klass_info, select, db)
        iterators.append(rel_cls)
    return iterators


class TenantModelIterable(ModelIterable):
    # need to be overridden on because get_related_populators()

    def __iter__(self):
        queryset = self.queryset
        db = queryset.db
        compiler = queryset.query.get_compiler(using=db)
        # Execute the query. This will also fill compiler.select, klass_info,
        # and annotations.
        results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
        select, klass_info, annotation_col_map = (compiler.select, compiler.klass_info,
                                                  compiler.annotation_col_map)
        model_cls = klass_info['model']
        select_fields = klass_info['select_fields']
        model_fields_start, model_fields_end = select_fields[0], select_fields[-1] + 1
        init_list = [f[0].target.attname
                     for f in select[model_fields_start:model_fields_end]]
        related_populators = get_related_populators(klass_info, select, db)
        for row in compiler.results_iter(results):
            obj = model_cls.from_db(db, init_list, row[model_fields_start:model_fields_end])
            if related_populators:
                for rel_populator in related_populators:
                    rel_populator.populate(row, obj)
            if annotation_col_map:
                for attr_name, col_pos in annotation_col_map.items():
                    setattr(obj, attr_name, row[col_pos])

            # Add the known related objects to the model, if there are any
            if queryset._known_related_objects:
                for field, rel_objs in queryset._known_related_objects.items():
                    # Avoid overwriting objects loaded e.g. by select_related
                    if field.is_cached(obj):
                        continue
                    pk = getattr(obj, field.get_attname())
                    try:
                        rel_obj = rel_objs[pk]
                    except KeyError:
                        pass  # may happen in qs1 | qs2 scenarios
                    else:
                        setattr(obj, field.name, rel_obj)
            yield obj


class TenantQuerySet(QuerySet):

    def __init__(self, model=None, query=None, using=None, hints=None):
        super().__init__(model, query, using, hints)
        self._iterable_class = TenantModelIterable

    def filter_schemas(self, *schemas):
        conn = connections['etools']
        if schemas and schemas[0]:
            conn.set_schemas(schemas)
        else:
            conn.set_all_schemas()

        return self

    # def prefetch_related(self, *lookups):
    #     """
    #     Return a new QuerySet instance that will prefetch the specified
    #     Many-To-One and Many-To-Many related objects when the QuerySet is
    #     evaluated.
    #
    #     When prefetch_related() is called more than once, append to the list of
    #     prefetch lookups. If prefetch_related(None) is called, clear the list.
    #     """
    #     clone = self._chain()
    #     if lookups == (None,):
    #         clone._prefetch_related_lookups = ()
    #     else:
    #         for lookup in lookups:
    #             if isinstance(lookup, Prefetch):
    #                 lookup = lookup.prefetch_to
    #             lookup = lookup.split(LOOKUP_SEP, 1)[0]
    #             if lookup in self.query._filtered_relations:
    #                 raise ValueError('prefetch_related() is not supported with FilteredRelation.')
    #         clone._prefetch_related_lookups = clone._prefetch_related_lookups + lookups
    #     return clone
