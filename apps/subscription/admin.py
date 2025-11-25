from django.contrib import admin
from apps.subscription.models import SubscriptionPlan, UserSubscription
# Register your models here.

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

