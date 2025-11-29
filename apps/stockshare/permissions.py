from rest_framework.permissions import BasePermission
from apps.stockshare.models import ShareWith
from django.utils import timezone

class IsSubscriptionActive(BasePermission):
    message = "No subscription plan or insufficient connections."
    
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        if request.method != 'POST':
            return True
        
        # Check has remaining connections
        total_sharewith = ShareWith.objects.filter(owner=user).count()
        if user.connections > total_sharewith:
            return True
        
        # has any subscriptions activate 
        active_subscript = user.subscriptions.filter(status='active',end_date__gt=timezone.now()).first()
        if not active_subscript:
            return False
        
        # For unlimited connectioin
        if active_subscript.plan.connetion_limits == 0:
            return True
        # For limited connection
        if user.connections + active_subscript.plan.connetion_limits > total_sharewith :
            return True
 
        return False
     
class IsOwner(BasePermission):
    message = "You can only delete your own connections."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
