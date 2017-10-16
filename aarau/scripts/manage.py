"""Utility script for database management.
"""

import os
import sys
from contextlib import contextmanager

from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars

from aarau import resolve_env_vars
from aarau.env import load_dotenv_vars
from aarau.models import (
    Project, Membership, Plan,
    Site,
    Publication, Article, Classification, License, Contribution,
    Application, Page,
    User, UserEmail,
)
from aarau.yaml import (
    yaml_loader,
    tokenize,
    set_password
)


def usage(argv):
    """Displays script usage.
    """
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <command> <action> [var=value]\n'
          '(example: "%s \'development.ini#\' db seed")' % (cmd, cmd))
    sys.exit(1)


class DbCli(object):
    """CLI for database (PostgreSQL) management.
    """
    def __init__(self, settings):
        self.settings = settings

        # for migrate router
        self.migrate_table = 'migrations'
        self.migrate_dir = os.path.join(os.getcwd(), 'db', 'migrations')

    @contextmanager
    def _raw_db(self, db_kind):
        from copy import copy
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

        with self._db(db_kind) as db:
            datname = copy(db.database)
            db.database = 'template1'
            conn = db.get_conn()
            conn.set_isolation_level(
                ISOLATION_LEVEL_AUTOCOMMIT
            )
            yield (db, datname)

    @contextmanager
    def _db(self, db_kind):
        from aarau.models import db, init_db

        db[db_kind] = init_db(self.settings, db_kind)

        yield db[db_kind]

    def help(self):  # pylint: disable=no-self-use
        """Prints usage.
        """
        print('usage: db {help|init|seed|drop} [var=value]')
        sys.exit(1)

    def init(self):
        """Initializes database.
        """
        with self._raw_db('cardinal') as (db, datname):
            q = "SELECT 1 FROM pg_database WHERE datname='{}'".format(datname)
            if db.execute_sql(q).rowcount != 0:
                sys.exit(0)

            q = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
                datname,
                'UTF-8',
                'template0'
            )
            db.execute_sql(q)

    def migrate(self):
        """Migrates database schema.
        """
        from peewee_migrate import Router

        with self._db('cardinal') as db, db.atomic():
            router = Router(db, migrate_table=self.migrate_table,
                            migrate_dir=self.migrate_dir)
            router.run()

    def rollback(self):
        """Rollbacks a latest migration.
        """
        from peewee_migrate import Router

        with self._db('cardinal') as db, db.atomic():
            router = Router(db, migrate_table=self.migrate_table,
                            migrate_dir=self.migrate_dir)
            if router.done:
                router.rollback(router.done[-1])

    def seed(self):
        """Imports db seed records for development.
        """
        with self._db('cardinal') as db, db.atomic():
            with yaml_loader(self.settings) as loader:
                def load_data(klass, attributes):
                    """Loads data into database.
                    """
                    with tokenize(attributes) as (tokens, attributes):

                        obj = klass(**attributes)
                        obj.save()

                        with set_password(obj, attributes) as obj:
                            obj.save()

                            for k, f in tokens.items():
                                setattr(obj, k, f(obj))
                                obj.save()

                # db/seeds/*.yml
                # TODO: import all files in db/seeds/*.yml
                # `order` sensitive
                models = [
                    Plan, Classification, License,
                    Project,
                    Publication, Article,
                    Application, Page,
                    Site,
                    User, UserEmail, Membership, Contribution,
                ]

                for model in models:
                    # pylint: disable=no-member,protected-access
                    table = model._meta.db_table
                    seed_yml = os.path.join(os.getcwd(), 'db', 'seeds',
                                            '{}.yml'.format(table))
                    if os.path.isfile(seed_yml):
                        data = loader(seed_yml)
                        for attributes in data[table]:
                            load_data(model, attributes)

    def drop(self):
        """Drops database.
        """
        with self._raw_db('cardinal') as (db, datname):
            q = "SELECT 1 FROM pg_database WHERE datname='{}'".format(datname)
            if db.execute_sql(q).rowcount == 0:
                sys.exit(0)

            q = 'DROP DATABASE {0}'.format(datname)
            db.execute_sql(q)


def main(argv=sys.argv):
    """The Main interface.
    """
    if len(argv) < 4:
        usage(argv)
    config_uri = argv[1]
    command = argv[2]
    action = argv[3]
    options = parse_vars(argv[4:])

    setup_logging(config_uri)
    load_dotenv_vars()

    # TODO: parse command and actions
    if command not in ('db',):
        raise Exception('Run with valid command {db} :\'(')

    shared_actions = ('help', 'init', 'drop')
    err_msg = 'Run with valid action {0!s} :\'('
    if command == 'db':
        db_actions = shared_actions + ('migrate', 'rollback', 'seed')
        if action not in db_actions:
            raise Exception(err_msg.format('|'.join(db_actions)))

    settings = get_appsettings(config_uri, options=options)
    settings = resolve_env_vars(dict(settings))

    cli = '{0}{1}'.format(command.capitalize(), 'Cli')
    c = globals()[cli](settings)
    getattr(c, action.lower())()
