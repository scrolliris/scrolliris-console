from pyramid.httpexceptions import HTTPNotFound

from aarau.models import (  # pylint: disable=unused-import
    Site,
    Project,
    Application,
    Publication,
    License,
    Classification,
)


def get_site(slug, project=None):
    """Gets a site by type belongs to the porject.

    If it does not exist, raises HTTPNotFound error.
    """
    if not project:
        return None
    try:
        site = Site.select().where(
            Site.slug == slug,
            Site.project_id == project.id).get()  # pylint: disable=no-member
    except Site.DoesNotExist:  # pylint: disable=no-member
        raise HTTPNotFound
    return site


def get_sites(type_, limit=10):
    instance_type = type_.capitalize()
    instance_class = globals()[instance_type]

    sites = Site.select()

    if type_ == 'application':
        sites = Site.select(  # pylint: disable=no-member
            Site, Project, instance_class
        ).join(
            instance_class,
            on=(Site.instance_id == instance_class.id).alias(type_)
        ).switch(Site).join(
            Project
        )
    else:
        sites = Site.select(  # pylint: disable=no-member
            Site, Project, instance_class, License, Classification
        ).join(
            instance_class,
            on=(Site.instance_id == instance_class.id).alias(type_)
        ).switch(Site).join(
            Project
        ).switch(Publication).join(
            License,
            on=(Publication.license_id == License.id)
        ).switch(Publication).join(
            Classification,
            on=(Publication.classification_id == Classification.id)
        )
    sites = sites.where(
        Site.instance_type == instance_type
    )

    if limit > 0:
        sites = sites.limit(limit)

    return sites


def get_publication_sites_with_params(query):
    query = query.replace('%', '\\%')
    query = query.replace('_', '\\_')
    sites = get_sites('publication', -1).where(
        Publication.name ** '%{:s}%'.format(query))
    return sites
