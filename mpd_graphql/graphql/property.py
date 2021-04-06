import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Property as PropertyModel, \
    PropertyType as PropertyTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input


# noinspection PyMethodParameters
class PropertyType(DjangoObjectType):
    class Meta:
        model = PropertyTypeModel


# noinspection PyMethodParameters
class Property(DjangoObjectType):
    class Meta:
        model = PropertyModel


class PropertyTypeInput(NamedInput):
    description = graphene.String()


class PropertyInput(NamedInput):
    property_type = graphene.Field(PropertyTypeInput)
    int_value = graphene.Int()
    float_value = graphene.Float()
    text_value = graphene.String()
    unit = graphene.String()


# noinspection PyMethodParameters,PyMethodMayBeStatic
class PropertyQuery(graphene.ObjectType):
    properties = graphene.List(Property)
    property_types = graphene.List(PropertyType)

    def resolve_properties(root, info) -> List[PropertyModel]:
        return PropertyModel.objects.all()

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


class PropertyMutation(graphene.ObjectType):
    update_property = UpdateProperty.Field()
    update_property_type = UpdatePropertyType.Field()
