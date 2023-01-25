from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_nonnegative(value):
    if value < 0:
        raise ValidationError(
            _("This field cannot be negative"),
            params={"value": value},
        )
