from django.db import models
from tree_queries.models import TreeNode

from .attribute import Attribute
from .identifier import Identifier
from .organization import Organization
from .process import Process, ProcessStep
from .property import Property
from .tracker import Tracker


class MaterialType(TreeNode):
    name = models.TextField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class MaterialSpecification(TreeNode, Tracker):
    class Meta:
        ordering = ('name',)
        unique_together = (('name', 'parent'),)

    name = models.TextField()
    description = models.TextField(null=True)
    version = models.TextField(null=True)

    material_type = models.ForeignKey(MaterialType,
                                      on_delete=models.SET_NULL,
                                      null=True)
    attributes = models.ManyToManyField(Attribute)
    identifiers = models.ManyToManyField(Identifier)
    properties = models.ManyToManyField(Property)

    supplier = models.ForeignKey(Organization,
                                 on_delete=models.SET_NULL,
                                 null=True)

    #process_methods_used_in = models.ManyToManyField('ProcessMethod',
    #                                                 through='ProcessMethodMaterialSpecification')

    def __str__(self):
        return self.name


class MaterialSpecificationDataFile(Tracker):
    specification = models.ForeignKey(MaterialSpecification,
                                      related_name='data_files',
                                      on_delete=models.CASCADE)
    file = models.FileField()


class Material(Tracker):
    name = models.TextField()
    description = models.TextField(null=True)

    specification = models.ForeignKey(MaterialSpecification,
                                      on_delete=models.SET_NULL,
                                      null=True)

    process = models.ForeignKey(Process,
                                related_name='materials_out',
                                on_delete=models.SET_NULL,
                                null=True)
    process_step = models.ForeignKey(ProcessStep,
                                     related_name='materials_out',
                                     on_delete=models.SET_NULL,
                                     null=True)

    attributes = models.ManyToManyField(Attribute)
    identifiers = models.ManyToManyField(Identifier)
    properties = models.ManyToManyField(Property)

    def __str__(self):
        return self.name


class MaterialDataFile(Tracker):
    material = models.ForeignKey(Material,
                                 related_name='data_files',
                                 on_delete=models.CASCADE)
    file = models.FileField()

