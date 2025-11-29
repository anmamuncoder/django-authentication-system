from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.stockshare.models import ShareWith
from apps.stockshare.serializers import ShareWithSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from .permissions import IsSubscriptionActive ,IsOwner
# Create your views here.

class ShareWithView(ModelViewSet): 
    serializer_class = ShareWithSerializer
    permission_classes = [IsAuthenticated,IsOwner,IsSubscriptionActive]

    def handle_exception(self, exception): 
        if isinstance(exception, PermissionDenied): 
            for permission in self.permission_classes:
                if hasattr(permission, 'message'):
                    message = permission.message 
            return Response({"success": False, "message": message},status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exception)
    
    def get_queryset(self):
        return ShareWith.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        raise PermissionDenied("You cant't update shared connecitons!")
    
    def perform_destroy(self, instance): 
        user1 = instance.owner
        user2 = instance.shared_user
 
        ShareWith.objects.filter(owner=user1, shared_user=user2).delete()
        ShareWith.objects.filter(owner=user2, shared_user=user1).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        