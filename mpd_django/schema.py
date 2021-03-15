import graphene

from mpd_graphql.graphql.attribute import AttributeQuery
from mpd_graphql.graphql.user import UserMutation, UserQuery


class Query(
    AttributeQuery,
    UserQuery,
):
    pass


class Mutation(
    UserMutation,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
