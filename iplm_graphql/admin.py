from django import forms
from django.contrib import admin
from feincms3.admin import TreeAdmin
import json


from .models import \
    Attribute, \
    MaterialSpecification, MaterialType, \
    ProcessMethod, ProcessMethodStep, ProcessType, \
    PropertySpecification, PropertyType


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)



@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    #form = movenodeform_factory(Attribute)
    list_display = ('name',)


@admin.register(MaterialSpecification)
class MaterialSpecificationAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProcessMethodForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    version = forms.CharField(max_length=50)


@admin.register(ProcessMethod)
class ProcessMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    form = ProcessMethodForm


class ProcessMethodStepForm(forms.ModelForm):
    name = forms.CharField(max_length=100)


@admin.register(ProcessMethodStep)
class ProcessMethodStepAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('created_by', 'created_at', 'modified_by', 'modified_at',)
    form = ProcessMethodStepForm


@admin.register(ProcessType)
class ProcessTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


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


