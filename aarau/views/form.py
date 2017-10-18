from pyramid.i18n import TranslationStringFactory
from wtforms.form import Form
from wtforms.csrf.core import CSRF as _CSRF


_ = TranslationStringFactory('form')


class CSRF(_CSRF):
    """CSRF utility extends pyramid's builtin csrf."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csrf_context = None

    def setup_form(self, form):
        self.csrf_context = form.meta.csrf_context
        return super(CSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_token_field):
        return self.csrf_context.get_csrf_token()

    def validate_csrf_token(self, form, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')


USERNAME_PATTERN = r'\A[a-z][a-z0-9\_\-]+\Z'
PASSWORD_PATTERN = r'(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])'


class SecureForm(Form):  # pylint: disable=too-few-public-methods
    """Form base class enables csrf protection."""

    class Meta:
        csrf = True
        csrf_class = CSRF


class FailureForm(SecureForm):
    """A form returns always failure at its validation."""

    def validate(self):
        return False


def build_form(klass, request, data=None):
    """Builder method builds a form."""
    form = klass(request.POST, data, meta={
        'csrf_context': request.session,
        'locales': ['en_US', 'en'],
    })
    return form
