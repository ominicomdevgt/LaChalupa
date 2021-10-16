

import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("La contraseña debe de conter almenos un numero, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Tu Contraseña debe de conter un numero  , 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Tu Contraseña debe de conterner almenos una Letra mayuscula, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Tu Contraseña debe de conterner almenos una Letra mayuscula, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Tu contraseña debe de conterner almenos una letra minuscula, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe de conterner almenos una letra minuscula, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Tu contraseña debe tener por lo menos un simbolo: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe tener por lo menos un simbolo: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )

