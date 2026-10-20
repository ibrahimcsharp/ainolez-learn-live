"""
MySQL backend that also runs on MariaDB 10.4 (the version XAMPP ships).

For local development only. Servers with MySQL 8 or MariaDB 10.5+ use
Django's normal backend: leave DB_ENGINE unset in their .env.
"""

from django.db.backends.mysql import base, features


class DatabaseFeatures(features.DatabaseFeatures):
    minimum_database_version = (10, 4)
    # INSERT ... RETURNING only exists from MariaDB 10.5.
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False


class DatabaseWrapper(base.DatabaseWrapper):
    features_class = DatabaseFeatures
