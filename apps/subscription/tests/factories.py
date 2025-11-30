import factory
import random
from factory import fuzzy
from decimal import Decimal
# Data Model
from apps.subscription.models import SubscriptionPlan,UserSubscription,Transaction
# Factory Model
from apps.users.tests.factories import UserFactory

# ---------------------------
# Subscription Plan Factory
# ---------------------------
class SubscriptionPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubscriptionPlan

    name = factory.Sequence(lambda n: f"Plan - {n}")
    description = factory.Faker('sentence')
    price = factory.LazyFunction(lambda : Decimal(random.randint(5,20)))
    type = factory.Iterator(['fixed','time_based'])
    connetion_limits  = factory.Iterator([3,5])
    duration_days = factory.Iterator([0,30])

# ---------------------------
# User Subscription Factory
# ---------------------------
class UserSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSubscription
    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(SubscriptionPlanFactory)
    status = factory.Iterator(['active','expired']) 
    
# ---------------------------
# Transaction Factory
# ---------------------------
class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
    user = factory.SubFactory(UserFactory)
    plan = factory.SubFactory(SubscriptionPlanFactory)
    bank_number = factory.Sequence(lambda n: f"Bank of-{n}")
    account_number =  "20210100110090"
    routing_number = "000444"

 