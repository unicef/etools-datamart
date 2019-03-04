from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import DatamartLoginView, DisconnectView, index, monitor, RequestAccessDoneView, RequestAccessView, whoami

urlpatterns = [
    path(r'', index, name='home'),
    path(r'monitor/', monitor, name='monitor'),
    path(r'login/', DatamartLoginView.as_view(template_name='login.html'), name='login'),
    path(r'logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path(r'request-access/', RequestAccessView.as_view(), name='request-access'),
    path(r'request-access/done/', RequestAccessDoneView.as_view(), name='request-access-done'),
    path(r'disconnect/', DisconnectView.as_view(next_page='/'), name='disconnect'),
    path(r'whoami/', whoami, name='whoami'),

]
