from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import action
from unicef_rest_framework.utils import get_query_string


class IQYConnectionMixin:

    @action(methods=['get'], detail=False)
    def iqy(self, request, version):
        qs = get_query_string(request.query_params, {'format': 'iqy'},
                              remove=['format'])
        url = f"{request.path}".replace('/iqy/', '/')

        iqy = """WEB
1
{host}{url}{qs}

Selection=AllTables
Formatting=html
PreFormattedTextToColumns=True
ConsecutiveDelimitersAsOne=True
SingleBlockTextImport=False
DisableDateRecognition=False

""".format(host=settings.ABSOLUTE_BASE_URL, request=request, qs=qs, url=url)
        return HttpResponse(iqy, content_type='text/plain')
