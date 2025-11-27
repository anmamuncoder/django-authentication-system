from django.db import transaction as transaction_db
from celery import shared_task
from apps.subscription.models import Transaction,UserSubscription
from apps.stockshare.models import ShareWith
from django.utils import timezone

@shared_task
def transaction_payment_approve(transaction_id): 

    try:
        transaction = Transaction.objects.select_related('user','plan').get(id=transaction_id)
    except Transaction.DoesNotExist:
        return {"success":False,"message":"Transaction does not exist!"}

    user = transaction.user
    plan = transaction.plan
    amount = plan.price
    
    activated_plan = UserSubscription.objects.filter(user=user,status='active').first()
    # if the same plan already activated
    if activated_plan and activated_plan.plan == plan:
        return {"success": False, "message": "This subscription plan is already active!"}

    with transaction_db.atomic(): 
        # --------------------------------
        #  REFUND LOGIC (time_based only)
        # --------------------------------
        if activated_plan and activated_plan.plan.type == 'time_based':
            spend_cost = 0
            if activated_plan.plan.connetion_limits > 0:
                """CASE 1: limited | How many balance will refund it will diside by per useres connection cost"""
                current_connection = ShareWith.objects.filter(owner=user).count() 
                extra_connection = max((current_connection - user.connections),0)

                per_connection_cost = activated_plan.plan.price / activated_plan.plan.connetion_limits
                spend_cost = (extra_connection * per_connection_cost) if extra_connection > 0  else 0 

            else:
                """CASE 2: unlimited | How many balance will deside by how long day usees"""
                used_days = (timezone.now() - activated_plan.start_date).days
                per_day_cost =  activated_plan.plan.price / activated_plan.plan.duration_days
                spend_cost = max(used_days * per_day_cost, 0)
            
            spend_cost = min(spend_cost, activated_plan.plan.price)
            reminder_cost = activated_plan.plan.price - spend_cost

            # Refunding user balance 
            user.balance += reminder_cost
            user.save(update_fields=['balance'])
            activated_plan.status = 'expired'
            activated_plan.end_date = timezone.now()
            activated_plan.save(update_fields=['status', 'end_date'])


        """        
        :rtype: Final Trunsaction in bank + balance
        """
        user.refresh_from_db()

        bank_deduct = max(amount - user.balance, 0) # How many balance will cut from bank
        user.balance = max(user.balance - amount, 0)

        # subscription plan include for the user
        user_subscription = UserSubscription.objects.create(user=user,plan=plan,status='active')
        user.save(update_fields=['balance'])

        # Update transaction status    
        transaction.status = 'confirmed'
        transaction.save(update_fields=['status'])

        return {'success':True,'user_balance':float(user.balance ), "bank_deduct":float(bank_deduct)}

 