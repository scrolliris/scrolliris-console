from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms import validators as v, ValidationError

from aarau.models import Plan
from aarau.views.form import SecureForm, build_form


NAMESPACE_PATTERN = r'\A[a-z][a-z0-9\_\-]+[a-z0-9]\Z'


class ProjectFormBaseMixin(object):
    name = StringField('Name', [
        v.Required(),
        v.Length(min=3, max=64),
    ])
    namespace = StringField('Namespace', [
        v.Required(),
        v.Regexp(NAMESPACE_PATTERN),
        v.Length(min=5, max=16),
    ])
    description = TextAreaField('Description', [
        v.Optional(),
        v.Length(max=1600),
    ])


class NewProjectForm(ProjectFormBaseMixin, SecureForm):
    submit = SubmitField('Create')


def new_project_form(req):
    class ANewProjectForm(NewProjectForm):
        def validate_namespace(self, field):  # pylint: disable=no-self-use
            from aarau.models.project import Project

            project = Project.select().where(
                Project.namespace == field.data).first()
            if project:
                raise ValidationError('Namespace is already taken.')

    return build_form(ANewProjectForm, req)


class EditProjectForm(ProjectFormBaseMixin, SecureForm):
    plan = SelectField('Plan', [
        v.Required(),
    ], choices=Plan.as_choices)

    submit = SubmitField('Update')


def edit_project_form(req, project):
    class AEditProjectForm(EditProjectForm):
        pass

    return build_form(AEditProjectForm, req, project)
