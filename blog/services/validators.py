import re

from django.core.exceptions import ValidationError

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.findall('\d', value):
        raise ValidationError('Password must contain at least one digit.')
    if not re.findall('[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not re.findall('[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')