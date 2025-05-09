from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)


from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View, CreateView


from accounts.email_thread import EmailThread
from accounts.forms import CustomLoginForm, RegisterForm, CustomPasswordResetForm
from accounts.models import CustomUser, Profile


USER = get_user_model()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    subject = "فعال‌سازی حساب کاربری"
    message = render_to_string(
        "accounts/emails/account_activation_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )

    email = EmailMessage(
        subject,
        message,
        to=[user.email],
    )
    EmailThread(email).start()


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(self.request, "با موفقیت خارج شدید")

        return redirect("pages:home")


class LoginView(AuthLoginView):
    form_class = CustomLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        # changing this part might cause problem in activating account with email
        response = super().form_valid(form)
        send_activation_email(self.object, self.request)
        messages.success(
            self.request, "ایمیلی حاوی لینک تایید حساب برای شما ارسال گردید"
        )
        return response


class PasswordChangeView(AuthPasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        messages.success(self.request, "رمز عبور با موفقیت تغییر کرد")

        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "accounts/password_reset.html"
    success_url = reverse_lazy("pages:home")
    email_template_name = "accounts/emails/password_reset_email.html"

    def form_valid(self, form):
        messages.success(
            self.request, "ایمیلی حاوی لینک تغییر رمز برای شما ارسال گردید"
        )

        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        messages.success(self.request, "رمز عبور با موفقیت تغییر کرد")

        return super().form_valid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = USER.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, USER.DoesNotExist) as e:
            print("Error decoding or finding user:", e)
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            messages.success(
                self.request, "اکانت شما با موفقیت تایید شد لطفا وارد شوید"
            )
        else:
            messages.success(
                self.request, "لینک فعال‌سازی معتبر نیست یا قبلاً استفاده شده ❌"
            )

        return redirect("accounts:login")
