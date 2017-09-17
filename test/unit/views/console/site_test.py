# pylint: disable=unused-argument
"""Unit tests for site view actions in console
"""
import pytest

from aarau.views.console.site.action import application_site_view_badge


@pytest.fixture(autouse=True)
def setup(config):
    """Setup
    """
    pass


def test_application_site_badge_without_type(users, dummy_request):
    """Test badge view without `type` query param
    """
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_badge_missing_project(users, dummy_request):
    """Test badge view unknown project
    """
    from webob.multidict import MultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = MultiDict({'type': 'application'})
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.matchdict = {
        'project_id': 0,  # invalid
        'id': site.id,
    }
    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_badge_missing_site(users, dummy_request):
    """Test badge view unknown site
    """
    from webob.multidict import MultiDict
    from pyramid.httpexceptions import HTTPNotFound

    user = users['oswald']
    dummy_request.user = user
    dummy_request.params = MultiDict({'type': 'application'})
    project = user.projects[0]
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': 0,  # invalid
    }
    with pytest.raises(HTTPNotFound):
        application_site_view_badge(dummy_request)


def test_application_site_badge(users, dummy_request):
    """Test badge view
    """
    from webob.multidict import MultiDict

    user = users['oswald']
    project = user.projects[0]
    site = project.application_sites[0]
    dummy_request.user = user
    dummy_request.params = MultiDict({'type': 'application'})
    dummy_request.matchdict = {
        'project_id': project.id,
        'id': site.id,
    }
    res = application_site_view_badge(dummy_request)
    assert project == res['project']
    assert site == res['site']
    assert site.application == res['application']
