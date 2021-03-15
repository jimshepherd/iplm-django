from django.db import models

from .tracker import Tracker


class PropertyType(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


# Add Tracker
class Property(Tracker):
    property_type = models.ForeignKey(PropertyType,
                                      on_delete=models.SET_NULL,
                                      null=True)
    integer_value = models.IntegerField()
    float_value = models.IntegerField()
    text_value = models.TextField()
    unit = models.TextField()

    def __str__(self):
        if self.property_type is not None:
            return self.property_type.name
        return ''
