import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Identifier as IdentifierModel, \
    IdentifierType as IdentifierTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input


# noinspection PyMethodParameters
class IdentifierType(DjangoObjectType):
    class Meta:
        model = IdentifierTypeModel


# noinspection PyMethodParameters
class Identifier(DjangoObjectType):
    class Meta:
        model = IdentifierModel


class IdentifierTypeInput(NamedInput):
    description = graphene.String()
    parent = graphene.InputField(lambda: IdentifierTypeInput)


class IdentifierInput(NamedInput):
    identifier_type = graphene.InputField(IdentifierTypeInput)
    value = graphene.String()


# noinspection PyMethodParameters,PyMethodMayBeStatic
class IdentifierQuery(graphene.ObjectType):
    identifiers = graphene.List(Identifier)
    identifier_types = graphene.List(IdentifierType)

    def resolve_identifiers(root, info) -> List[IdentifierModel]:
        return IdentifierModel.objects.all()

    def resolve_identifier_types(root, info) -> List[IdentifierTypeModel]:
        return IdentifierTypeModel.objects.all()


class UpdateIdentifier(graphene.Mutation):
    class Arguments:
        identifier = IdentifierInput(required=True)

    identifier = graphene.Field(Identifier)

    def mutate(root, info, identifier=None):
        ident_model = get_model_by_id_or_name(IdentifierModel, identifier)
        if ident_model is None:
            ident_model = IdentifierModel()
        update_model_from_input(ident_model, identifier)
        ident_model.save()
        return UpdateIdentifier(identifier=ident_model)


class UpdateIdentifierType(graphene.Mutation):
    class Arguments:
        identifier_type = IdentifierTypeInput(required=True)

    identifier_type = graphene.Field(IdentifierType)

    def mutate(root, info, identifier_type=None):
        type_model = get_model_by_id_or_name(IdentifierTypeModel, identifier_type)
        if type_model is None:
            type_model = IdentifierTypeModel()
        update_model_from_input(type_model, identifier_type)
        type_model.save()
        return UpdateIdentifierType(identifier_type=type_model)


class IdentifierMutation(graphene.ObjectType):
    update_identifier = UpdateIdentifier.Field()
    update_identifier_type = UpdateIdentifierType.Field()
