from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def validate_year(value):
    if value < 1886 or value > datetime.date.today().year:
        raise ValidationError(
            _('%(value)s is not a proper year'),
            params={'value': value},
        )
