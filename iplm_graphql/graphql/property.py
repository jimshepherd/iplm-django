import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Property as PropertyModel, \
    PropertySpecification as PropertySpecificationModel, \
    PropertyType as PropertyTypeModel

from .base import NamedInput, FixResolutionMixin
from .helpers import get_model_by_id_or_name, update_model_from_input


# noinspection PyMethodParameters
class PropertySpecification(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = PropertySpecificationModel


# noinspection PyMethodParameters
class PropertyType(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = PropertyTypeModel


# noinspection PyMethodParameters
class Property(FixResolutionMixin, DjangoObjectType):
    class Meta:
        model = PropertyModel


class PropertyTypeInput(NamedInput):
    description = graphene.String()
    parent = graphene.Field(lambda: PropertyTypeInput)


class PropertySpecificationInput(NamedInput):
    description = graphene.String()
    property_type = graphene.Field(PropertyTypeInput)
    values = graphene.JSONString()
    unit = graphene.String()


class PropertyInput(NamedInput):
    property_type = graphene.Field(PropertyTypeInput)
    specification = graphene.Field(PropertySpecificationInput)
    int_value = graphene.Int()
    float_value = graphene.Float()
    text_value = graphene.String()
    unit = graphene.String()


# noinspection PyMethodParameters,PyMethodMayBeStatic
class PropertyQuery(graphene.ObjectType):
    properties = graphene.List(Property)
    property_specifications = graphene.List(PropertySpecification)
    property_types = graphene.List(PropertyType)

    def resolve_properties(root, info) -> List[PropertyModel]:
        return PropertyModel.objects.all()

    def resolve_property_specifications(root, info) -> List[PropertySpecificationModel]:
        return PropertySpecificationModel.objects.all()

    def resolve_property_types(root, info) -> List[PropertyTypeModel]:
        return PropertyTypeModel.objects.all()


class UpdateProperty(graphene.Mutation):
    class Arguments:
        property = PropertyInput(required=True)

    property = graphene.Field(Property)

    def mutate(root, info, property=None):
        prop_model = get_model_by_id_or_name(PropertyModel, property)
        if prop_model is None:
            prop_model = PropertyModel()
        update_model_from_input(prop_model, property)
        prop_model.save()
        return UpdateProperty(property=prop_model)


class UpdatePropertyType(graphene.Mutation):
    class Arguments:
        property_type = PropertyTypeInput(required=True)

    property_type = graphene.Field(PropertyType)

    def mutate(root, info, property_type=None):
        type_model = get_model_by_id_or_name(PropertyTypeModel, property_type)
        if type_model is None:
            type_model = PropertyTypeModel()
        update_model_from_input(type_model, property_type)
        type_model.save()
        return UpdatePropertyType(property_type=type_model)


class UpdatePropertySpecification(graphene.Mutation):
    class Arguments:
        property_specification = PropertySpecificationInput(required=True)

    property_specification = graphene.Field(PropertySpecification)

    def mutate(root, info, property_specification=None):
        spec_model = get_model_by_id_or_name(PropertySpecificationModel, property_specification)
        if spec_model is None:
            spec_model = PropertySpecificationModel()
        update_model_from_input(spec_model, property_specification)
        spec_model.save()
        return UpdatePropertySpecification(property_specification=spec_model)


class PropertyMutation(graphene.ObjectType):
    update_property = UpdateProperty.Field()
    update_property_specification = UpdatePropertySpecification.Field()
    update_property_type = UpdatePropertyType.Field()
