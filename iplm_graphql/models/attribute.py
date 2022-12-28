from django.db import models
from tree_queries.models import TreeNode


class Attribute(TreeNode):
    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'parent'),)

    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name
