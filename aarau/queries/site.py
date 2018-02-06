from aarau.models import (  # noqa  # pylint: disable=unused-import
    Site,
    Project,
    Application,
    Publication,
    License,
    Classification,
)


def get_sites(type_, limit=10):
    instance_type = type_.capitalize()
    instance_class = globals()[instance_type]

    sites = Site.select().join(
        instance_class,
        on=(Site.instance_id == instance_class.id).alias(type_)
    ).switch(Site).join(
        Project
    )
    if type_ == 'application':
        sites = sites.select(
            Site, Project, instance_class
        )
    else:
        sites = sites.select(
            Site, Project, instance_class, License, Classification
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
