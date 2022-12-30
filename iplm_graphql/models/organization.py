from django.db import models
from tree_queries.models import TreeNode

from .tracker import Tracker


class OrganizationType(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


# Add Tracker
class Organization(TreeNode, Tracker):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    # addresses from Address
    org_types = models.ManyToManyField(OrganizationType,
                                       related_name='organizations')

    def __str__(self):
        return self.name


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

    def __str__(self):
        if self.organization is not None:
            return self.organization.__str__()
        return self.street
