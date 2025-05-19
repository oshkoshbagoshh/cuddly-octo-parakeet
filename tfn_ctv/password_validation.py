#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexityValidator:
    """
    Validate that the password meets complexity requirements:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    
    def __init__(self, min_upper=1, min_lower=1, min_digits=1, min_special=1):
        self.min_upper = min_upper
        self.min_lower = min_lower
        self.min_digits = min_digits
        self.min_special = min_special
    
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password) or sum(1 for c in password if c.isupper()) < self.min_upper:
            raise ValidationError(
                _("Password must contain at least %(min_upper)d uppercase letter.") % {'min_upper': self.min_upper},
                code='password_no_upper',
            )
        if not re.search(r'[a-z]', password) or sum(1 for c in password if c.islower()) < self.min_lower:
            raise ValidationError(
                _("Password must contain at least %(min_lower)d lowercase letter.") % {'min_lower': self.min_lower},
                code='password_no_lower',
            )
        if not re.search(r'[0-9]', password) or sum(1 for c in password if c.isdigit()) < self.min_digits:
            raise ValidationError(
                _("Password must contain at least %(min_digits)d digit.") % {'min_digits': self.min_digits},
                code='password_no_digit',
            )
        special_chars = set('!@#$%^&*()_+-=[]{}|;:,.<>?/~`"\'\\')
        if sum(1 for c in password if c in special_chars) < self.min_special:
            raise ValidationError(
                _("Password must contain at least %(min_special)d special character.") % {'min_special': self.min_special},
                code='password_no_special',
            )
    
    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_upper)d uppercase letter, "
            "%(min_lower)d lowercase letter, %(min_digits)d digit, and "
            "%(min_special)d special character."
        ) % {
            'min_upper': self.min_upper,
            'min_lower': self.min_lower,
            'min_digits': self.min_digits,
            'min_special': self.min_special,
        }