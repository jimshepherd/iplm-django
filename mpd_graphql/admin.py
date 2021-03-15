from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Attribute


@admin.register(Attribute)
class AttributeAdmin(TreeAdmin):
    form = movenodeform_factory(Attribute)
