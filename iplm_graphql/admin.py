from django import forms
from django.contrib import admin
from feincms3.admin import TreeAdmin
import json


from .models import \
    Attribute, \
    Equipment, EquipmentType,\
    Identifier, IdentifierType,\
    Material, MaterialDataFile, \
    MaterialSpecification, MaterialSpecificationDataFile, MaterialType, \
    Organization, OrganizationType, Address,\
    Process, ProcessStep, ProcessDataFile, ProcessDataSet, \
    ProcessMethod, ProcessMethodStep, ProcessType, \
    ProcessMaterial, ProcessMethodMaterialSpecification, \
    Property, PropertySpecification, PropertyType


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(Attribute)
class AttributeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


@admin.register(Identifier)
class IdentifierAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(IdentifierType)
class IdentifierTypeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(MaterialDataFile)
class MaterialDataFileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(MaterialSpecification)
class MaterialSpecificationAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(MaterialSpecificationDataFile)
class MaterialSpecificationDataFileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(MaterialType)
class MaterialTypeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


@admin.register(Organization)
class OrganizationAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(ProcessStep)
class ProcessStepAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(ProcessDataFile)
class ProcessDataFileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(ProcessDataSet)
class ProcessDataSetAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(ProcessMaterial)
class ProcessMaterialAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


class ProcessMethodForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    version = forms.CharField(max_length=50)


@admin.register(ProcessMethod)
class ProcessMethodAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    form = ProcessMethodForm


@admin.register(ProcessMethodMaterialSpecification)
class ProcessMethodMaterialSpecificationAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


class ProcessMethodStepForm(forms.ModelForm):
    name = forms.CharField(max_length=100)


@admin.register(ProcessMethodStep)
class ProcessMethodStepAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    form = ProcessMethodStepForm


@admin.register(ProcessType)
class ProcessTypeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)


@admin.register(PropertyType)
class PropertyTypeAdmin(TreeAdmin):
    list_display = ('indented_title', 'move_column', 'name',)


class PropertySpecificationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    values = forms.JSONField(encoder=PrettyJSONEncoder)
    unit = forms.CharField(max_length=50)


@admin.register(PropertySpecification)
class PropertySpecificationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    form = PropertySpecificationForm


