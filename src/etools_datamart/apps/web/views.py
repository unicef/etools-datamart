import re

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core import validators
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.template.response import TemplateResponse

from etools_datamart.apps.etl.models import EtlTask
from etools_datamart.config.settings import env


def index(request):
    context = {'page': 'index', 'title': 'eTools Datamart'}
    return TemplateResponse(request, 'index.html', context)


@login_required
def monitor(request):
    context = {'tasks': EtlTask.objects.all(),
               'subscriptions': request.user.subscriptions,
               'page': 'monitor'}
    return TemplateResponse(request, 'monitor.html', context)


def whoami(request):
    if request.user.is_authenticated:
        return HttpResponse(request.user.email)
    return HttpResponse('')


class DisconnectView(LogoutView):
    def get_next_page(self):  # pragma: no cover
        return env('DISCONNECT_URL')


class EmailField2(forms.EmailField):
    default_validators = [validators.validate_email,
                          RegexValidator(re.compile('@unicef.org$'),
                                         message='email must be @unicef.org')]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['class'] = 'input100'
        return attrs


# class RequestAccessForm(forms.Form):
#     email = EmailField2()
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         synchronizer = Synchronizer(keep_records=True)
#         results = synchronizer.fetch_users("(mail eq '%s')" % email)
#         if not list(results.all()):
#             raise ValidationError('Cannot find this email')
#         return email
#
#
# message = """Dear %(user)s,
#
# below the password to access eTools Datamart
#
# **%(password)s**
#
# Please note that this password should be used with 'Local Account login' only if you have problems with 'Azure login'.
#
# [[login]]
#
# """
#
#
# class RequestAccessDoneView(TemplateView):
#     template_name = 'request_access.html'
#
#     def get_context_data(self, **kwargs):
#         return super().get_context_data(done=True)
#
#
# class RequestAccessFailView(TemplateView):
#     template_name = 'request_access.html'
#
#     def get_context_data(self, **kwargs):
#         return super().get_context_data(fail=True)
#
#
# class RequestAccessView(FormView, ProcessFormView):
#     template_name = 'request_access.html'
#     form_class = RequestAccessForm
#
#     def get_success_url(self):
#         return reverse('request-access-done')
#
#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         user = User.objects.get(email=email)
#         password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
#         user.set_password(password)
#         user.save()
#         kwargs = {'user': user, 'password': password, 'login': reverse('login')}
#         conn = get_connection('django.core.mail.backends.smtp.EmailBackend', False)
#         send_mail(
#             'Your eTools Datamart password',
#             message=message % kwargs,
#             from_email='noreply@unicef.org',
#             recipient_list=[kwargs['user'].email],
#             html_message=markdown(message % kwargs,
#                                   extensions=['markdown.extensions.smarty',
#                                               WikiLinkExtension(base_url='http://datamart.unicef.io/')
#                                               ]
#                                   ),
#             fail_silently=False,
#             connection=conn,
#         )
#         return super().form_valid(form)


class DatamartLoginView(LoginView):

    def get_context_data(self, **kwargs):
        kwargs['settings'] = settings
        return super().get_context_data(**kwargs)


# class PasswordResetForm2(PasswordResetForm):
#     def send_mail(self, subject_template_name, email_template_name,
#                   context, from_email, to_email, html_email_template_name=None):
#         subject = loader.render_to_string(subject_template_name, context)
#         # Email subject *must not* contain newlines
#         subject = ''.join(subject.splitlines())
#         body = loader.render_to_string(email_template_name, context)
#         conn = get_connection('django.core.mail.backends.smtp.EmailBackend', False)
#
#         email_message = EmailMultiAlternatives(subject, body, from_email, [to_email],
#                                                connection=conn)
#         if html_email_template_name is not None:
#             html_email = loader.render_to_string(html_email_template_name, context)
#             email_message.attach_alternative(html_email, 'text/html')
#
#         email_message.send()
#
#     def get_users(self, email):
#         email = self.cleaned_data['email']
#         synchronizer = Synchronizer(keep_records=True)
#         results = synchronizer.fetch_users("(mail eq '%s')" % email)
#         if not list(results.all()):
#             return []
#         return UserModel._default_manager.filter(**{'%s__iexact' % UserModel.get_email_field_name(): email})
