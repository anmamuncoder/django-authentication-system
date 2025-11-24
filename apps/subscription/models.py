from django.db import models
from django.utils import timezone
from apps.inventory.models import BaseModel 
from .constants import SELECT_PLAN_STATUS, SELECT_PLAN_TYPE, SELECT_TRANSACTION_STATUS
from apps.users.models import User
# Create your models here.

# --------------------------
# Subscription Plan Model
# --------------------------
class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    connetion_limits = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=SELECT_PLAN_TYPE, default='time_based')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

# --------------------------
# User Subscription Model
# --------------------------
class UserSubscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='user_subscriptions')
    status = models.CharField(max_length=20, choices=SELECT_PLAN_STATUS, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True, editable=False)

    @property
    def remaining_days(self):
        if not self.end_date:
            return None
        
        remaining = (self.end_date - timezone.now()).days
        return remaining if remaining > 0 else 0

    def save(self, *args, **kwargs):
        # Set end_date based on plan type
        if self.plan.type == 'time_based' and self.status == 'active':
            if not self.end_date:
                self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)

        # Update user's connections if plan is fixed 
        elif self.plan.type == 'fixed' and self.status == 'active':
            self.user.connections += self.plan.connetion_limits
            self.user.save()
            self.end_date = None # No EndDate for Fixed plans

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"
    
# --------------------------
# Subscription Transaction Model
# --------------------------
class Transaction(BaseModel): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50)
    success = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=SELECT_TRANSACTION_STATUS, default='pending')

    def __str__(self):
        return f"Transaction {self.id} - {self.user.username} - {self.status}"
    
    