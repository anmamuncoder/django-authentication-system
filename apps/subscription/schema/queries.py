import graphene
from .types import SubscriptionPlanType, UserSubscriptionType
from apps.subscription.models import SubscriptionPlan, UserSubscription

# -------------------------
# Subscription Plan Queries
# -------------------------
class SubscriptionPlanQuery(graphene.ObjectType):
    subscription_plans = graphene.List(SubscriptionPlanType)

    def resolve_subscription_plans(self, info):
        return SubscriptionPlan.objects.filter(active=True)

