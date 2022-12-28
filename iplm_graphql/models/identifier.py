from django.db import models
from tree_queries.models import TreeNode

from .tracker import Tracker


class IdentifierType(TreeNode):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Identifier(Tracker):
    identifier_type = models.ForeignKey(IdentifierType,
                                        related_name='identifiers',
                                        on_delete=models.SET_NULL,
                                        null=True)
    value = models.TextField()
