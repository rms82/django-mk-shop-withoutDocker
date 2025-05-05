from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager
from accounts.validators import IranianPhoneNumberValidator


# Create your models here.
class UserType(models.IntegerChoices):
    customer = 1, 'customer'
    admin = 2, 'admin'
    superuser = 3, 'superuser'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(_("firstname"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("lastname"), max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        _("phone number"),
        max_length=12,
        null=True,
        blank=True,
        validators=[
            IranianPhoneNumberValidator(),
        ],
    )
    image = models.ImageField(upload_to='profile/img/', null=True, blank=True, default='default_profile.jpg')

    @property
    def fullname(self):
        return str(self.first_name + " " + self.last_name).title()

    def __str__(self):
        return self.user.email

    def reset_image_to_default(self):
        self.image = 'default_profile.jpg'
        self.save()

    def save(self, *args, **kwargs):
        if not self.first_name:
            self.first_name = ""

        if not self.last_name:
            self.last_name = ""
        
        return super().save(*args, **kwargs)

