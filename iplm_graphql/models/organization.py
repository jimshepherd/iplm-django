from django.db import models
from tree_queries.models import TreeNode

from .tracker import Tracker


class OrganizationType(models.Model):
    name = models.TextField()
    description = models.TextField()


# Add Tracker
class Organization(TreeNode, Tracker):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    # addresses from Address
    org_types = models.ManyToManyField(OrganizationType,
                                       related_name='organizations')


class Address(Tracker):
    organization = models.ForeignKey(Organization,
                                     related_name='addresses',
                                     on_delete=models.CASCADE,
                                     null=True)
    street = models.TextField(null=True)
    street2 = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    country = models.TextField(null=True)
    zip = models.TextField(null=True)
