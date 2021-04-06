from django.db import models

from .material import Material
from .process import Process, ProcessStep
from .property import Property
from .tracker import Tracker


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
    properties = models.ManyToManyField(Property)
