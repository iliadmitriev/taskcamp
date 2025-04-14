"""
Database simple router module.

Attributes:
    SimpleDBRouter: class for simple router.
"""

from typing import Optional

from django.contrib.contenttypes.models import ContentType


class SimpleDBRouter:
    """Simple database router.

    Used for split queries between master and read only replica databases.
    """

    def db_for_read(self, model: ContentType, **hints) -> Optional[str]:
        """Forward read queries to replica connection.

        Args:
            model: model object link (content type)
            **hints:

        Returns:
            (str): name of database connection to be used for read queries
        """
        return "replica"

    def db_for_write(self, model: ContentType, **hints) -> str:
        """Forward write queries to master connection.

        Args:
            model: model object link (content type)
            **hints:

        Returns:
            (str) name of database connection to be used for write queries
        """
        return "master"

    def allow_relation(self, obj1: ContentType, obj2: ContentType, **hints) -> Optional[bool]:
        """Return the possibility to proceed create relation between models.

        Args:
            obj1: Instance of first model
            obj2: Instance of second model
            **hints:

        Returns:
            (bool): True - if it's possible to create relation between models
                    False - otherwise
        """
        return True

    def allow_migrate(self, db: str, app_label: str, model_name: str = None, **hints) -> Optional[bool]:
        """Check if migration for model cold be applied to database db.

        Args:
            db: database name
            app_label: name of application
            model_name: name of model in application `app_label`
            **hints:

        Returns:
            (bool): True - if migration for model cold be applied to database db.
                    False - otherwise
        """
        return True
