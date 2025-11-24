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

# -------------------------
#  User Subscription Queries with JWT Authentication 
# ------------------------- 
class UserSubscriptionQuery(graphene.ObjectType):
    user_subscriptions = graphene.List(UserSubscriptionType)

    def resolve_user_subscriptions(self, info):
        user = info.context.user 
        
        # User must be authenticated
        if user.is_anonymous:
            raise Exception("Authentication required")

        return UserSubscription.objects.filter(user=user)
