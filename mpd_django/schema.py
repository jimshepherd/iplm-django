import graphene

from mpd_graphql.graphql.attribute import AttributeQuery, AttributeMutation
from mpd_graphql.graphql.equipment import EquipmentQuery, EquipmentMutation
from mpd_graphql.graphql.identifier import IdentifierQuery, IdentifierMutation
from mpd_graphql.graphql.organization import OrganizationQuery, OrganizationMutation
from mpd_graphql.graphql.material import MaterialQuery, MaterialMutation
from mpd_graphql.graphql.product_specification import MICQuery, MICMutation
from mpd_graphql.graphql.process import ProcessQuery, ProcessMutation
from mpd_graphql.graphql.property import PropertyQuery, PropertyMutation
from mpd_graphql.graphql.user import UserMutation, UserQuery


class Query(
    AttributeQuery,
    EquipmentQuery,
    IdentifierQuery,
    MaterialQuery,
    MICQuery,
    OrganizationQuery,
    ProcessQuery,
    PropertyQuery,
    UserQuery,
):
    pass


class Mutation(
    AttributeMutation,
    EquipmentMutation,
    IdentifierMutation,
    MaterialMutation,
    MICMutation,
    OrganizationMutation,
    ProcessMutation,
    PropertyMutation,
    UserMutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
