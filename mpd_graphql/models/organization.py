from django.db import models

from .tracker import Tracker


class OrganizationType(models.Model):
    name = models.TextField()
    description = models.TextField()


# Add Tracker
class Organization(Tracker):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    #addresses
    org_types = models.ManyToManyField(OrganizationType)
    parent = models.ForeignKey('Organization',
                               on_delete=models.SET_NULL,
                               null=True)


class Address(Tracker):
    organization = models.ForeignKey(Organization,
                                     related_name='addresses',
                                     on_delete=models.CASCADE)
    street = models.TextField(null=True)
    street2 = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    zip = models.TextField(null=True)
