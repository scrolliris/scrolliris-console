from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from aarau.models.article import Article
from aarau.queries.project import get_project
from aarau.queries.site import get_site
from aarau.views.filter import login_required
from aarau.views.console.article.form import (
    build_article_editor_form,
    build_article_config_form,
)


def save_content(req, article):
    form = build_article_editor_form(req, article)

    if form.validate():
        with req.db.cardinal.atomic():
            article.content = form.content.data or ''

            article.save()

    return (article, form.errors)


def save_meta(req, article):
    form = build_article_config_form(req, article)

    if form.validate():
        with req.db.cardinal.atomic():
            article.title = form.title.data
            article.scope = 'private' if not form.scope.data else 'public'
            # optional
            article.path = form.path.data

            article.save()

    return (article, form.errors)


def handle_post(req):
    namespace = req.matchdict.get('namespace')
    slug = req.matchdict.get('slug')

    code = req.params.get('code')  # update

    project = get_project(namespace, user=req.user)
    site = get_site(slug, project=project)

    if site.type != 'publication':
        raise HTTPNotFound

    publication = site.instance
    if code:
        article = publication.articles.where(
            Article.code == code).get()
    else:
        code = Article.grab_unique_code()
        article = Article(
            code=code,
            path=code,
            title='',
            copyright='',
            publication=publication)

    context = req.params.get('context', None)
    _ = req.translate
    if context == 'editor':
        (article, errors) = save_content(req, article)
    elif context == 'config':
        (article, errors) = save_meta(req, article)
    else:
        raise HTTPNotFound

    message = _('article.save.failure')
    if not errors:
        message = _('article.save.success')

    return dict(
        status='ok',
        code=article.code,
        errors=errors,
        message=message)


@view_config(route_name='api.console.article.config',
             request_method='POST',
             renderer='json')
@login_required
def api_article_config(req):
    try:
        return handle_post(req)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'status': 'error',
            'error': 'The resource was not found'})


@view_config(route_name='api.console.article.editor',
             request_method='POST',
             renderer='json')
@login_required
def api_article_editor(req):
    try:
        return handle_post(req)
    except HTTPNotFound:
        return Response(status=404, json_body={
            'status': 'error',
            'error': 'The resource was not found'})
