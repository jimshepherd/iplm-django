from django.db import models
from tree_queries.models import TreeNode

from .attribute import Attribute
from .identifier import Identifier
from .organization import Organization
from .property import Property
from .tracker import Tracker


class EquipmentType(TreeNode):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Equipment(Tracker):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    equipment_type = models.ForeignKey(EquipmentType,
                                       related_name='equipment',
                                       on_delete=models.SET_NULL,
                                       null=True)
    organization = models.ForeignKey(Organization,
                                     related_name='equipment',
                                     on_delete=models.SET_NULL,
                                     null=True)

    attributes = models.ManyToManyField(Attribute,
                                        related_name='equipment')
    identifiers = models.ManyToManyField(Identifier,
                                         related_name='equipment')
    properties = models.ManyToManyField(Property,
                                        related_name='equipment')

    def __str__(self):
        return self.name

