from django.db import models

from .tracker import Tracker


class PropertyType(models.Model):
    name = models.TextField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class PropertySpecification(Tracker):
    name = models.TextField()
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType,
                                      on_delete=models.SET_NULL,
                                      null=True)
    values = models.JSONField()
    unit = models.TextField(null=True)

    def __str__(self):
        return self.name


class Property(Tracker):
    property_type = models.ForeignKey(PropertyType,
                                      on_delete=models.SET_NULL,
                                      null=True)
    specification = models.ForeignKey(PropertySpecification,
                                      on_delete=models.SET_NULL,
                                      null=True)

    int_value = models.IntegerField(null=True)
    float_value = models.FloatField(null=True)
    text_value = models.TextField(null=True)
    unit = models.TextField(null=True)

    def __str__(self):
        if self.property_type is not None:
            return self.property_type.name
        return ''
