from django.db import models

from .material import Material, MaterialSpecification
from .process import Process, ProcessMethod, ProcessMethodStep, ProcessStep
from .property import Property
from .tracker import Tracker


class ProcessMethodMaterialSpecification(Tracker):
    process_method = models.ForeignKey(ProcessMethod,
                                       related_name='process_method_material_specifications_in',
                                       on_delete=models.CASCADE)
    process_method_step = models.ForeignKey(ProcessMethodStep,
                                            related_name='process_method_material_specifications_in',
                                            on_delete=models.CASCADE,
                                            null=True)
    material_specification = models.ForeignKey(MaterialSpecification,
                                               related_name='process_method_material_specifications_used_in',
                                               on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property,
                                        related_name='process_method_material_specifications')

    def __str__(self):
        if self.process_method is not None and self.material_specification is not None:
            return f'{self.process_method.__str__()}' \
                   f'-{self.material_specification.__str__()}'
        return ''


class ProcessMaterial(Tracker):
    process = models.ForeignKey(Process,
                                related_name='materials_in',
                                on_delete=models.CASCADE)
    process_step = models.ForeignKey(ProcessStep,
                                     related_name='materials_in',
                                     on_delete=models.CASCADE,
                                     null=True)
    material = models.ForeignKey(Material,
                                 related_name='processes_used_in',
                                 on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property,
                                        related_name='process_materials')

    def __str__(self):
        if self.process is not None and self.material is not None:
            return f'{self.process.__str__()}-{self.material.__str__()}'
        return ''
