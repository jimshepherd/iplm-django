import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import Attribute as AttributeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input


# noinspection PyMethodParameters
class Attribute(DjangoObjectType):
    class Meta:
        model = AttributeModel


class AttributeInput(NamedInput):
    description = graphene.String()
    parent = graphene.InputField(lambda: AttributeInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class AttributeQuery(graphene.ObjectType):
    attributes = graphene.List(Attribute,
                               parent=AttributeInput())

    def resolve_attributes(root, info,
                           parent=None) -> List[AttributeModel]:
        parent_model = get_model_by_id_or_name(AttributeModel, parent)
        if parent_model is not None:
            return parent_model.descendants()
        return AttributeModel.objects.all()


class UpdateAttribute(graphene.Mutation):
    class Arguments:
        attribute = AttributeInput(required=True)

    attribute = graphene.Field(Attribute)

    def mutate(root, info, attribute=None):
        attr_model = get_model_by_id_or_name(AttributeModel, attribute)
        if attr_model is None:
            attr_model = AttributeModel()
        update_model_from_input(attr_model, attribute)
        attr_model.save()
        return UpdateAttribute(attribute=attr_model)


class AttributeMutation(graphene.ObjectType):
    update_attribute = UpdateAttribute.Field()
