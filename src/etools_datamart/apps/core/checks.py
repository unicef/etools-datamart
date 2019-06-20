# import sys
#
# from django.core import checks
# from django.db import ProgrammingError
#
# #
# # @checks.register()
# # def check_services(app_configs, **kwargs):
# #     try:
# #         from unicef_rest_framework.models import Service
# #         created, deleted, total = Service.objects.load_services()
# #         sys.stdout.write(f"{total} services found. {created} new. {deleted} deleted")
# #     except ProgrammingError:
# #         pass
# #     return []
