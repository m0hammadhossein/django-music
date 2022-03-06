from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, LoginView as AuthLogin, LogoutView as AuthLogout, \
    PasswordChangeView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from accounts.forms import SignUp as SignUpForm
from accounts.mixins import LogoutRequiredMixin
from accounts.token import account_activation_token


class LoginView(LogoutRequiredMixin, AuthLogin):
    """
    Added mixin logout to not show the login page to logged in users
    """
    pass


class LogoutView(LoginRequiredMixin, AuthLogout):
    """
    Added mixin login  to show the logout page to logged in users,
    Added redirect for logout
    """
    next_page = reverse_lazy('accounts:login')


class PasswordReset(PasswordResetView):
    """
    Changed redirect url
    """
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordChange(PasswordChangeView):
    """
        Changed redirect url
    """
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordResetConfirm(PasswordResetConfirmView):
    """
        Changed redirect url
    """
    success_url = reverse_lazy('accounts:password_reset_complete')


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:register_done')

    def form_valid(self, form):
        self.object = form.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری'
        message = render_to_string('registration/email_template.html', {
            'user': self.object,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
            'token': account_activation_token.make_token(self.object),
        })
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
        return HttpResponseRedirect(self.get_success_url())


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            context = {'msg': 'حساب شما با موفقیت فعال شد.'}
        else:
            context = {'msg': 'این لینک منقضی شده است.'}
        return render(request, 'registration/activate.html', context=context)


class RegisterDone(TemplateView):
    template_name = 'registration/register_done.html'


class Profile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'registration/profile.html'
    fields = ('first_name', 'last_name', 'image')
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)