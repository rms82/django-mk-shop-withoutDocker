from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    PasswordResetForm,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from accounts.email_thread import EmailThread

User = get_user_model()


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("آدرس ایمیل یا رمز عبور اشتباه است"),
        "inactive": _("این اکانت غیر فعال است"),
        "not_verify": _("این اکانت تایید نشده است"),
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError(
                self.error_messages["not_verify"],
                code="inactive",
            )


class RegisterForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("کاربری با این ایمیل وجود ندارد ")
        return email

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):

        subject = render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        EmailThread(email_message).start()
