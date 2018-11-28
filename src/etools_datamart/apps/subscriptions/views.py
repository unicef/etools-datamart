import json

from django.forms import ModelForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.apps.subscriptions.models import Subscription


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['type', 'kwargs']


@csrf_exempt
def subscribe(request, etl_id):
    code = 200
    values = {'status': "", 'detail': ""}
    try:
        user = request.user
        payload = json.loads(request.body)
        form = SubscriptionForm(data=payload)
        if form.is_valid():
            etl = EtlTask.objects.get(id=etl_id)
            s, created = Subscription.objects.update_or_create(user=user,
                                                               content_type=etl.content_type,
                                                               kwargs=payload.get("kwargs", ''),
                                                               defaults={
                                                                   'type': payload["type"]
                                                               })
            values['status'] = {True: "created", False: "updated"}[created]
            values['detail'] = {"id": s.id,
                                "type": s.type,
                                "type_label": s.get_type_display(),
                                }
        else:
            values['detail'] = "Invalid request"
            values['error'] = form.errors
            code = 400

    except EtlTask.DoesNotExist as e:
        values['detail'] = f"Invalid task id `{etl_id}`"
        values['error'] = str(e)
        code = 404
    except Exception as e:
        values['error'] = type(e).__name__
        values['detail'] = str(e)
        code = 500
    return JsonResponse(values, status=code)
