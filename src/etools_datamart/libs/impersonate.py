from django.contrib.auth import get_user_model


def queryset(request):
    return get_user_model().objects.exclude(id=request.user.id).exclude(is_superuser=True).order_by("username")
