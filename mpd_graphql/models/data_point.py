from django.db import models

from .tracker import Tracker


class DataPointType(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)


class DataPoint(Tracker):
    # Normalize data_type if found useful
    data_point_type = models.ForeignKey(DataPointType,
                                        related_name='data_points',
                                        on_delete=models.CASCADE)
    units = models.TextField(null=True)

    # Use integer_data field for boolean data
    integer_data = models.IntegerField()
    float_data = models.FloatField()
    text_data = models.TextField()
