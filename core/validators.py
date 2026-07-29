import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_no_emoji(value):
    if re.search(r"[\U0001F000-\U0001FFFF]", value):
        raise ValidationError(_("Não aceita emojis."))
    return value
