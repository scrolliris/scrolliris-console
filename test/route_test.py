import pytest


@pytest.fixture(autouse=True)
def setup(request, config):  # pylint: disable=unused-argument
    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False)

    request.addfinalizer(teardown)


def test_routing_to_favicon(dummy_app):
    res = dummy_app.get('/favicon.ico', status=200)
    assert 200 == res.status_code


@pytest.mark.usefixtures('login')
def test_routing_to_favicon_as_logged_in_user(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/favicon.ico', status=200)
        assert 200 == res.status_code


def test_routing_to_humans(dummy_app):
    res = dummy_app.get('/humans.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_humans_as_logged_in_user(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/humans.txt', status=200)
        assert 200 == res.status_code


def test_routing_to_robots(dummy_app):
    res = dummy_app.get('/robots.txt', status=200)
    assert 200 == res.status_code


def test_routing_to_robots_as_logged_in_user(dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        app = dummy_app.switch_target('console')
        res = app.get('/robots.txt', status=200)
        assert 200 == res.status_code


def test_routing_to_console_application_settings_badges(
        dummy_app, login_as, users):
    user = users['oswald']
    with login_as(user):
        project = user.projects[0]
        site = project.application_sites[0]
        url = '/projects/{}/sites/{}/settings/badges?type=application'.format(
            project.id, site.id)
        app = dummy_app.switch_target('console')
        res = app.get(url, status=200)
        assert 200 == res.status_code
