import pytest


@pytest.fixture(autouse=True)
def setup(config):  # pylint: disable=unused-argument
    pass


def test_forbidden_redirect_as_logged_in_user(users, dummy_request):
    from pyramid.httpexceptions import HTTPFound
    from aarau.views.filter import forbidden_redirect

    dummy_request.user = users['oswald']
    res = forbidden_redirect(dummy_request)

    assert isinstance(res, HTTPFound)
    assert '302 Found' == res.status
    assert 'http://example.org/' == res.location


def test_forbidden_redirect(dummy_request):
    from pyramid.httpexceptions import HTTPFound
    from aarau.views.filter import forbidden_redirect

    dummy_request.user = None
    res = forbidden_redirect(dummy_request)

    assert isinstance(res, HTTPFound)
    assert '302 Found' == res.status
    assert dummy_request.session.pop_flash('failure')
    assert 'http://example.org/login' == res.location
