from django.conf import settings
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from unicef_rest_framework.utils import get_query_string

IQY = """WEB
1
http://datamart.unicef.io/api/latest/hact/?format=iqy

Selection=AllTables
Formatting=html
PreFormattedTextToColumns=True
ConsecutiveDelimitersAsOne=True
SingleBlockTextImport=False
DisableDateRecognition=False
DisableRedirections=True
"""


class IQYConnectionMixin:

    @swagger_auto_schema(responses={200: "OK"})
    @action(methods=['get'], detail=False)
    def iqy(self, request, version):
        """Returns .iqy file to be used as Excel Web Connection """
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
DisableRedirections=True
""".format(host=settings.ABSOLUTE_BASE_URL, request=request, qs=qs, url=url)
        return HttpResponse(iqy, content_type='text/plain')
