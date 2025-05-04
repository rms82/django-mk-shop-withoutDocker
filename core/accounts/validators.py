from django.core.validators import RegexValidator


class IranianPhoneNumberValidator(RegexValidator):
    regex = r"^(09|9)\d{9}$"
    message = 'شماره تلفن باید به فرمت "09xxxxxxxxx" باشد'
