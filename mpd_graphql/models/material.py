from django.db import models

from .attribute import Attribute
from .identifier import Identifier
from .organization import Organization
from .property import Property
from .tracker import Tracker


# Could be renamed to MaterialSpecification
class MaterialSpecification(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)
    version = models.TextField(null=True)

    parent = models.ForeignKey('MaterialSpecification',
                               on_delete=models.SET_NULL,
                               null=True)

    attributes = models.ManyToManyField(Attribute)
    identifiers = models.ManyToManyField(Identifier)
    properties = models.ManyToManyField(Property)

    supplier = models.ForeignKey(Organization,
                                 on_delete=models.SET_NULL,
                                 null=True)

    def __str__(self):
        return self.name


class Material(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)

    specification = models.ForeignKey(MaterialSpecification,
                                      on_delete=models.SET_NULL,
                                      null=True)

    process = models.ForeignKey('Process',
                                on_delete=models.SET_NULL,
                                null=True)

    attributes = models.ManyToManyField(Attribute)
    identifiers = models.ManyToManyField(Identifier)
    properties = models.ManyToManyField(Property)

    producer = models.ForeignKey(Organization,
                                 on_delete=models.SET_NULL,
                                 null=True)

    def __str__(self):
        return self.name
