from django.db import models

from .material import Material
from .process import Process
from .property import Property
from .tracker import Tracker


class ProcessMaterial(Tracker):
    process = models.ForeignKey(Process,
                                on_delete=models.CASCADE)
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)


