from django.db import models
from tree_queries.models import TreeNode

from .data_set import DataSet
from .equipment import Equipment, EquipmentType
from .organization import Organization
from .property import Property, PropertySpecification
from .tracker import Tracker
from .user import User


class ProcessType(models.Model):
    name = models.TextField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class ProcessMethod(TreeNode, Tracker):
    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'parent'),)

    name = models.TextField()
    description = models.TextField(null=True)
    version = models.TextField(null=True)

    process_type = models.ForeignKey(ProcessType,
                                     on_delete=models.SET_NULL,
                                     null=True)
    equipment_type = models.ForeignKey(EquipmentType,
                                       on_delete=models.SET_NULL,
                                       null=True)
    properties = models.ManyToManyField(Property)
    property_specs = models.ManyToManyField(PropertySpecification)

    material_specs_in = models.ManyToManyField('MaterialSpecification',
                                               through='ProcessMethodMaterialSpecification')

    # steps

    def __str__(self):
        return self.name


class ProcessMethodStep(TreeNode, Tracker):
    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'parent'),)

    name = models.TextField()
    description = models.TextField()
    order = models.IntegerField(default=0)

    method = models.ForeignKey(ProcessMethod,
                               related_name='steps',
                               on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)
    property_specs = models.ManyToManyField(PropertySpecification)

    def __str__(self):
        return self.name


class Process(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)

    process_type = models.ForeignKey(ProcessType,
                                     on_delete=models.SET_NULL,
                                     null=True)
    method = models.ForeignKey(ProcessMethod,
                               on_delete=models.SET_NULL,
                               null=True)

    producer = models.ForeignKey(Organization,
                                 on_delete=models.SET_NULL,
                                 null=True)
    equipment = models.ForeignKey(Equipment,
                                  on_delete=models.SET_NULL,
                                  null=True)
    operator = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True)
    properties = models.ManyToManyField(Property)

    # materials_in
    # materials_out
    # process_steps

    def __str__(self):
        return self.name


class ProcessStep(TreeNode, Tracker):
    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'parent'),)

    name = models.TextField()
    description = models.TextField()
    order = models.IntegerField()

    process = models.ForeignKey(Process,
                                related_name='steps',
                                on_delete=models.CASCADE)
    method_step = models.ForeignKey('ProcessMethodStep',
                                    on_delete=models.SET_NULL,
                                    null=True)

    # Following fields duplicate method steps so might be removable
    # parent = models.ForeignKey('ProcessStep',
    #                            on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)

    def __str__(self):
        return self.name


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
