from django.contrib import admin
from apps.subscription.models import SubscriptionPlan, UserSubscription,Transaction
# Register your models here.
from .tasks import transaction_payment_approve

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'connetion_limits', 'active','created_at','updated_at')
    search_fields = ('name',)
    list_filter = ('active',)

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status','created_at','updated_at')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('status',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','plan','amount','status','created_at')
    actions = ('make_approved','make_rejected')

    def make_approved(self,request,queryset):
        count = 0
        for transaction in queryset:
            if transaction.status != 'confirmed':
                transaction_payment_approve.delay(transaction.id)
                count += 1
        self.message_user(request, f"{count} transaction(s) have been approved.")
    make_approved.short_description = "Make Approved Payments"

    def make_rejected(self,request,queryset):
        return queryset.update(status='rejected')
    make_rejected.short_description = "Make Rejected Payments"
    