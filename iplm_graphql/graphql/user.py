import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphql_jwt
from graphql_jwt.shortcuts import create_refresh_token, get_token

from ..models import User as UserModel

from .base import NamedInput


class User(DjangoObjectType):
    class Meta:
        model = UserModel

    name = graphene.String()

    def resolve_name(self, info):
        return self.get_full_name()


class UserInput(NamedInput):
    pass


# noinspection PyMethodParameters,PyMethodMayBeStatic
class UserQuery(graphene.ObjectType):
    current_user = graphene.Field(User)

    def resolve_current_user(root, info) -> UserModel:
        user = info.context.user
        print('current user', user)
        if user.is_anonymous:
            raise GraphQLError('Authentication Failure: Not signed inauth')
        return user


# noinspection PyMethodMayBeStatic
class CreateUser(graphene.Mutation):
    user = graphene.Field(User)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = UserModel(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user,
                          token=token,
                          refresh_token=refresh_token)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

