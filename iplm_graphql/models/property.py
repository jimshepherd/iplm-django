from django.db import models
from tree_queries.models import TreeNode

from .tracker import Tracker


class PropertyType(TreeNode):
    name = models.TextField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class PropertySpecification(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)
    property_type = models.ForeignKey(PropertyType,
                                      related_name='property_specifications',
                                      on_delete=models.SET_NULL,
                                      null=True)
    values = models.JSONField()
    unit = models.TextField(null=True)

    def __str__(self):
        return self.name


class Property(Tracker):
    property_type = models.ForeignKey(PropertyType,
                                      related_name='properties',
                                      on_delete=models.SET_NULL,
                                      null=True)
    specification = models.ForeignKey(PropertySpecification,
                                      related_name='properties',
                                      on_delete=models.SET_NULL,
                                      null=True)

    int_value = models.IntegerField(null=True)
    float_value = models.FloatField(null=True)
    text_value = models.TextField(null=True)
    unit = models.TextField(null=True)

    def __str__(self):
        name = ''
        if self.property_type is not None:
            name = self.property_type.__str__()
        elif self.specification is not None:
            name = self.specification.property_type.__str__()
        value = ''
        if self.int_value is not None:
            value = self.int_value
        elif self.float_value is not None:
            value = self.float_value
        elif self.text_value is not None:
            value = self.text_value
        unit = ''
        if self.unit is not None:
            unit = self.unit
        return f'{name}={value} {unit}'
