import graphene

from iplm_graphql.graphql.attribute import AttributeQuery, AttributeMutation
from iplm_graphql.graphql.equipment import EquipmentQuery, EquipmentMutation
from iplm_graphql.graphql.identifier import IdentifierQuery, IdentifierMutation
from iplm_graphql.graphql.organization import OrganizationQuery, OrganizationMutation
from iplm_graphql.graphql.material import MaterialQuery, MaterialMutation
# from iplm_graphql.graphql.product_specification import ProductSpecificationQuery, ProductSpecificationMutation
from iplm_graphql.graphql.process import ProcessQuery, ProcessMutation
from iplm_graphql.graphql.property import PropertyQuery, PropertyMutation
from iplm_graphql.graphql.user import UserMutation, UserQuery


class Query(
    AttributeQuery,
    EquipmentQuery,
    IdentifierQuery,
    MaterialQuery,
    # ProductSpecificationQuery,
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
    # ProductSpecificationMutation,
    OrganizationMutation,
    ProcessMutation,
    PropertyMutation,
    UserMutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
