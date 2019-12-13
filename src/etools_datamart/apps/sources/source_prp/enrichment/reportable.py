from etools_datamart.apps.sources.source_prp.models import IndicatorIndicatorblueprint, IndicatorReportable


def convert_string_number_to_float(num):
    return float(num.replace(',', '')) if type(num) == str else float(num)


def get_calculated_baseline(self):
    if not self.baseline['v']:
        return 0.0

    if self.blueprint.unit == IndicatorIndicatorblueprint.NUMBER:
        return convert_string_number_to_float(self.baseline['v'])
    else:
        return convert_string_number_to_float(self.baseline['v']) / convert_string_number_to_float(self.baseline['d'])


def get_calculated_target(self):
    if not self.target['v']:
        return 0.0

    if self.blueprint.unit == IndicatorIndicatorblueprint.NUMBER:
        return convert_string_number_to_float(self.target['v'])
    else:
        return convert_string_number_to_float(self.target['v']) / convert_string_number_to_float(self.target['d'])


IndicatorReportable.calculated_baseline = property(get_calculated_baseline)
IndicatorReportable.calculated_target = property(get_calculated_target)
