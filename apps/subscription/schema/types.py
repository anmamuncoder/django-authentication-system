import graphene
from graphene_django.types import DjangoObjectType 
from graphene import relay

from apps.subscription.models import SubscriptionPlan, UserSubscription, Transaction

class SubscriptionPlanType(DjangoObjectType):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"

class UserSubscriptionType(DjangoObjectType):
    class Meta:
        model = UserSubscription
        fields = "__all__"

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = "__all__"
        # - begin Queryset pagination, Relay style (edges/node)
        interfaces = (relay.Node,) 

    