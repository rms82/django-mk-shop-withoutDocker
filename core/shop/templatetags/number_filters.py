from django import template

register = template.Library()

def arabic_to_persian(num):
    arabic_digits = '0123456789'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    translation_table = str.maketrans(arabic_digits, persian_digits)
    return num.translate(translation_table)

@register.filter
def format_persian_price(value):
    if not isinstance(value, int):
        return value
    
    formatted_number = '{:,}'.format(value)
    
    persian_number = arabic_to_persian(formatted_number)
    
    return persian_number