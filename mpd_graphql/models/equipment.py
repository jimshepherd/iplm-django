from django.db import models

from .attribute import Attribute
from .identifier import Identifier
from .organization import Organization
from .property import Property
from .tracker import Tracker


class EquipmentType(models.Model):
    name = models.TextField()
    description = models.TextField()


class Equipment(Tracker):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    equipment_type = models.ForeignKey(EquipmentType,
                                       on_delete=models.SET_NULL,
                                       null=True)
    organization = models.ForeignKey(Organization,
                                     on_delete=models.SET_NULL,
                                     null=True)

    attributes = models.ManyToManyField(Attribute)
    identifiers = models.ManyToManyField(Identifier)
    properties = models.ManyToManyField(Property)
