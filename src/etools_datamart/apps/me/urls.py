from django.urls import path

from .views import ProfileView

urlpatterns = [
    path(r'', ProfileView.as_view(), name='profile'),

]
