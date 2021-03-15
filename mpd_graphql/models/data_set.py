from django.contrib.postgres.fields import ArrayField
from django.db import models

from .tracker import Tracker


class DataSet(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)


class DataSeries(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)
    data_set = models.ForeignKey(DataSet,
                                 on_delete=models.CASCADE)
    # Normalize series_type if found useful
    series_type = models.TextField(null=True)
    units = models.TextField(null=True)

    # Use integer_data field for boolean data
    integer_data = ArrayField(models.IntegerField())
    float_data = ArrayField(models.FloatField())
    text_data = ArrayField(models.TextField())
