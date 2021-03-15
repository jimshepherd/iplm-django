from django.db import models

from .tracker import Tracker


class IdentifierType(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Identifier(Tracker):
    identifier_type = models.ForeignKey(IdentifierType,
                                        on_delete=models.SET_NULL,
                                        null=True)
    value = models.TextField()

