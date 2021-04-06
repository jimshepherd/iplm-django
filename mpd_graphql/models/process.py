from django.db import models

from .data_set import DataSet
from .organization import Organization
from .property import Property
from .tracker import Tracker


class ProcessMethod(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)
    version = models.TextField(null=True)

    parent = models.ForeignKey('ProcessMethod',
                               on_delete=models.SET_NULL,
                               null=True)


class ProcessMethodStep(Tracker):
    name = models.TextField()
    description = models.TextField()
    method = models.ForeignKey(ProcessMethod,
                               related_name='steps',
                               on_delete=models.CASCADE)
    parent = models.ForeignKey('ProcessMethodStep',
                               on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    properties = models.ManyToManyField(Property)


# Add Tracker
class Process(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)

    method = models.ForeignKey(ProcessMethod,
                               on_delete=models.SET_NULL,
                               null=True)

    producer = models.ForeignKey(Organization,
                                 on_delete=models.SET_NULL,
                                 null=True)

    # materials_in
    # materials_out
    # process_steps


class ProcessStep(Tracker):
    name = models.TextField()
    description = models.TextField()
    process = models.ForeignKey(Process,
                                related_name='steps',
                                on_delete=models.CASCADE)
    method_step = models.ForeignKey('ProcessMethodStep',
                                    on_delete=models.SET_NULL,
                                    null=True)

    # Following fields duplicate method steps so might be removable
    parent = models.ForeignKey('ProcessStep',
                               on_delete=models.CASCADE)
    order = models.IntegerField()

    properties = models.ManyToManyField(Property)


class ProcessDataFile(Tracker):
    process = models.ForeignKey(Process,
                                related_name='data_files',
                                on_delete=models.CASCADE)
    file = models.FileField()


class ProcessDataSet(Tracker):
    process = models.ForeignKey(Process,
                                related_name='data_sets',
                                on_delete=models.CASCADE)
    data_set = models.ForeignKey(DataSet,
                                 on_delete=models.CASCADE)
    step = models.ForeignKey(ProcessStep,
                             on_delete=models.SET_NULL,
                             null=True)
    file = models.ForeignKey(ProcessDataFile,
                             on_delete=models.SET_NULL,
                             null=True)
