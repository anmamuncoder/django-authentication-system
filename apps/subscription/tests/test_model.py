import pytest
from typing import Tuple
from django.db import IntegrityError
from django.utils import timezone

# Data Model
from apps.subscription.models import SubscriptionPlan,UserSubscription,Transaction
# Data Factory
from apps.users.tests.factories import UserFactory
from .factories import SubscriptionPlanFactory,UserSubscriptionFactory,TransactionFactory


pytestmark = pytest.mark.django_db

# ---------------------------
# Facture for Reuseable data
# ---------------------------
@pytest.fixture
def plans() -> Tuple[SubscriptionPlan,SubscriptionPlan]: 
    # type(fixed) connetion_limits(3) duration_days(0)
    plan1 = SubscriptionPlanFactory() 
    # type(time_based) connetion_limits(5) duration_days(3)
    plan2 = SubscriptionPlanFactory() 
    return plan1, plan2

# -------------------------------
# Subscription Plan Model Test
# -------------------------------
def test_subscription_create():
    """
    Test creating a Subscription Plan 
    """
    plan1 = SubscriptionPlanFactory()
    assert plan1.id is not None
    assert plan1.type == 'fixed'
    assert plan1.connetion_limits is 3
    assert plan1.duration_days is 0
    assert str(plan1) == f"{plan1.name} - {plan1.price}"
    
    plan2 = SubscriptionPlanFactory()
    assert plan2.id is not None
    assert plan2.type == 'time_based'
    assert plan2.connetion_limits is 5
    assert plan2.duration_days is 30
    assert str(plan2) == f"{plan2.name} - {plan2.price}"
 
def test_subscription_update():
    """
    Test for subscription update
    """
    plan = SubscriptionPlanFactory()
    plan.name = "NewName"
    plan.description = "NewDescription"
    plan.price = 99
    plan.duration_days = 100
    plan.connetion_limits = 10
    plan.type = "time_based"
    plan.active = False
    plan.save()

    assert plan.name == "NewName"
    assert plan.description == "NewDescription"
    assert plan.price == 99
    assert plan.duration_days == 100
    assert plan.connetion_limits == 10
    assert plan.type == "time_based"
    assert plan.active == False

def test_subscription_delete():
    """
    Test for subscription Delete
    """
    plan = SubscriptionPlanFactory()
    plan_id = plan.id
    plan.delete()

    has = SubscriptionPlan.objects.filter(id=plan_id).exists()
    assert has == False

# -------------------------------
# User Subscription Plan Model Test
# -------------------------------
def test_user_subscription_create_with_status_None(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory()
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=fixed_plan)
    assert subscript.user  is user
    assert subscript.plan is fixed_plan
    assert subscript.status is None
    assert subscript.start_date.hour == timezone.now().hour
    assert subscript.start_date.minute == timezone.now().minute
    assert subscript.end_date is None
    assert str(subscript) == f"{subscript.user.username} - {subscript.plan.name} - {subscript.status}"

def test_user_subscription_create_with_status_Active_for_plan_Fixed(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory() 
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=fixed_plan,status='active')

    assert subscript.user  is user
    assert subscript.plan is fixed_plan
    assert subscript.status == 'expired'
    assert subscript.start_date.hour == timezone.now().hour
    assert subscript.start_date.minute == timezone.now().minute 
    assert subscript.end_date.hour == (subscript.start_date + timezone.timedelta(days=subscript.plan.duration_days)).hour
    assert str(subscript) == f"{subscript.user.username} - {subscript.plan.name} - {subscript.status}"
    
def test_user_subscription_create_with_status_Active_for_plan_TimeBase(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory()
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=timebase_plan,status='active')

    assert subscript.user  is user
    assert subscript.plan is timebase_plan
    assert subscript.status == 'active'
    assert subscript.start_date.hour == timezone.now().hour
    assert subscript.start_date.minute == timezone.now().minute 
    assert subscript.end_date.hour == (subscript.start_date + timezone.timedelta(days=subscript.plan.duration_days)).hour
    assert str(subscript) == f"{subscript.user.username} - {subscript.plan.name} - {subscript.status}"

def test_user_subscription_create_with_status_Expired_for_plan_Fixed(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory()
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=fixed_plan,status='expired')
    assert subscript.user  is user
    assert subscript.plan is fixed_plan
    assert subscript.status == 'expired'
    assert subscript.start_date.hour == timezone.now().hour
    assert subscript.start_date.minute == timezone.now().minute 
    assert subscript.end_date.minute == (subscript.start_date + timezone.timedelta(days=subscript.plan.duration_days)).minute
    assert str(subscript) == f"{subscript.user.username} - {subscript.plan.name} - {subscript.status}"

def test_user_subscription_create_with_status_Expired_for_plan_TimeBase(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory() 
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=fixed_plan,status='expired')
    assert subscript.user  is user
    assert subscript.plan is fixed_plan
    assert subscript.status == 'expired'
    assert subscript.start_date.hour == timezone.now().hour
    assert subscript.start_date.minute == timezone.now().minute 
    assert subscript.end_date.minute == (subscript.start_date + timezone.timedelta(days=subscript.plan.duration_days)).minute
    assert str(subscript) == f"{subscript.user.username} - {subscript.plan.name} - {subscript.status}"

def test_user_subscription_update_Active_to_Expired_TimeBase(plans):
    """
    Test for UserSubscription create
    """
    user = UserFactory() 
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=timebase_plan,status='active')
    assert subscript.user  is user
    assert subscript.plan is timebase_plan
    assert subscript.status == 'active' 
    assert subscript.start_date.date() == timezone.now().date() 
    assert subscript.end_date.day == (subscript.start_date + timezone.timedelta(days=subscript.plan.duration_days)).day
    
    subscript.status = 'expired'
    subscript.save()
    # assert subscript.end_date.day == 0
    assert subscript.end_date.date() == timezone.now().date()

def test_user_subscription_delete(plans):
    user = UserFactory() 
    fixed_plan, timebase_plan = plans

    subscript = UserSubscription.objects.create(user=user,plan=timebase_plan,status='active')
    subscript_id = subscript.id

    has = UserSubscription.objects.filter(id=subscript_id).exists()
    assert has is True

# -----------------------------------------
# Transaction Subscription Plan Model Test
# -----------------------------------------

def test_transaction_create(plans):
    """
    Test for Transaction Create
    """
    user = UserFactory()
    fixed_plan, timebase_plan = plans
    tran = Transaction.objects.create(user=user,plan=fixed_plan,amount=5,bank_name='ISLM',account_number="12",routing_number="00")

    assert tran.user is user
    assert tran.plan is fixed_plan
    assert str(tran) == f"Transaction {tran.id} - {user.username} - pending"

def test_transaction_update(plans):
    user = UserFactory()
    fixed_plan, timebase_plan = plans
    tran = Transaction.objects.create(user=user,plan=fixed_plan,amount=5,bank_name='ISLM',account_number="12",routing_number="00")

    assert tran.user is user
    assert tran.plan is fixed_plan

    user2 = UserFactory()
    tran.user = user2 
    tran.plan = timebase_plan

    assert tran.user is user2
    assert tran.plan is timebase_plan

def test_transaction_delete(plans):
    user = UserFactory()
    fixed_plan, timebase_plan = plans
    tran = Transaction.objects.create(user=user,plan=fixed_plan,amount=5,bank_name='ISLM',account_number="12",routing_number="00")
    tran_id = tran.id

    has = Transaction.objects.filter(id=tran_id).exists()
    assert has is True
