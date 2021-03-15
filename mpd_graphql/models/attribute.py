from django.db import models
from treebeard.mp_tree import MP_Node


# Use django-treebeard
class Attribute(MP_Node):
    name = models.TextField()
    description = models.TextField()

    node_order_by = ['name']

    def __str__(self):
        return self.name
