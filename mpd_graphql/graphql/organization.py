import graphene
from graphene_django import DjangoObjectType
from typing import List

from ..models import \
    Address as AddressModel, \
    Organization as OrganizationModel, \
    OrganizationType as OrganizationTypeModel

from .base import NamedInput
from .helpers import get_model_by_id_or_name, update_model_from_input


# noinspection PyMethodParameters
class Address(DjangoObjectType):
    class Meta:
        model = AddressModel


# noinspection PyMethodParameters
class OrganizationType(DjangoObjectType):
    class Meta:
        model = OrganizationTypeModel


# noinspection PyMethodParameters
class Organization(DjangoObjectType):
    class Meta:
        model = OrganizationModel


class AddressInput(NamedInput):
    street = graphene.String()
    street2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    zip = graphene.String()


class OrganizationTypeInput(NamedInput):
    description = graphene.String()


class OrganizationInput(NamedInput):
    description = graphene.String()
    parent = graphene.InputField(lambda: OrganizationInput)
    org_types = graphene.List(OrganizationTypeInput)
    addresses = graphene.List(AddressInput)


# noinspection PyMethodParameters,PyMethodMayBeStatic
class OrganizationQuery(graphene.ObjectType):
    organizations = graphene.List(Organization)
    organization_types = graphene.List(OrganizationType)

    def resolve_organizations(root, info) -> List[OrganizationModel]:
        return OrganizationModel.objects.all()

    def resolve_organization_types(root, info) -> List[OrganizationTypeModel]:
        return OrganizationTypeModel.objects.all()


class UpdateOrganization(graphene.Mutation):
    class Arguments:
        organization = OrganizationInput(required=True)

    organization = graphene.Field(Organization)

    def mutate(root, info, organization=None):
        org_model = get_model_by_id_or_name(OrganizationModel, organization)
        if org_model is None:
            org_model = OrganizationModel()
        update_model_from_input(org_model, organization, save_only_attrs=['addresses'])
        org_model.save()
        return UpdateOrganization(organization=org_model)


class UpdateOrganizationType(graphene.Mutation):
    class Arguments:
        organization_type = OrganizationTypeInput(required=True)

    organization_type = graphene.Field(OrganizationType)

    def mutate(root, info, organization_type=None):
        type_model = get_model_by_id_or_name(OrganizationTypeModel, organization_type)
        if type_model is None:
            type_model = OrganizationTypeModel()
        update_model_from_input(type_model, organization_type)
        type_model.save()
        return UpdateOrganizationType(organization_type=type_model)


class OrganizationMutation(graphene.ObjectType):
    update_organization = UpdateOrganization.Field()
    update_organization_type = UpdateOrganizationType.Field()
