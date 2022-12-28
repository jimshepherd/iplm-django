from django.db import models
from django_currentuser.db.models import CurrentUserField


class Tracker(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = CurrentUserField(related_name='created_%(class)s_set')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = CurrentUserField(related_name='modified_%(class)s_set',
                                   on_update=True)
