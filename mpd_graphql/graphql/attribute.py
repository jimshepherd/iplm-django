import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import Attribute as AttributeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name


class Attribute(DjangoObjectType):
    class Meta:
        model = AttributeModel
    parent: 'Attribute' = graphene.Field(lambda: Attribute)

    def resolve_parent(root, info):
        return root.get_parent()


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
            return parent_model.get_descendants()
        return AttributeModel.objects.all()
