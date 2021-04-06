from django.contrib.auth.models import User
from django.db import models


class Tracker(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='created_%(class)s_set',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,
                                    related_name='modified_%(class)s_set',
                                    on_delete=models.SET_NULL,
                                    null=True, blank=True)

    def save(self, *args, **kwargs):
        # print('Save args', args)
        # print('Save kwargs', kwargs)
        super().save(*args, **kwargs)
