import pytest


@pytest.fixture(autouse=True)
def setup(request, config, mailbox):  # pylint: disable=unused-argument
    mailbox.clean()

    # eager task (emulation)
    from aarau.tasks import worker
    worker.conf.update(task_always_eager=True)

    def teardown():
        worker.conf.update(task_always_eager=False)
        mailbox.clean()

    request.addfinalizer(teardown)


def test_signup(dummy_app):
    from pyramid_mailer import get_mailer

    res = dummy_app.get('/signup', status=200)
    res.charset = None

    user = {  # The Egg Twins
        'name': 'Leo The Egg Twins',
        'username': 'leotheegg',
        'email': 'leo@example.org',
        'password': 'yesYes!*2',
    }

    form = res.forms['signup']
    form['email'] = user['email']
    form['name'] = user['name']
    form['username'] = user['username']
    form['password'] = user['password']
    res = form.submit('submit', value='Create an account')

    assert '302 Found' == res.status
    res = res.follow(status=200)
    res.charset = None
    assert 'Your signup has been successfully requested' in \
        res.html.select_one('.success.message p')

    mailer = get_mailer(dummy_app.app.registry)
    message = mailer.outbox[0]
    assert [user['email']] == message.recipients
    assert 'Test <noreply@example.org>' == message.sender
    assert 'Activate your account' in message.subject
    assert 'You have successfully signed up to Scrolliris.' in message.body
