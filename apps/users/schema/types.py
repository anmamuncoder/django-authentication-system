import graphene
from graphene_django.types import DjangoObjectType
from apps.users.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email","phone_number",'first_name','last_name','photo','balance','connections')

