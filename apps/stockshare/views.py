from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.stockshare.models import ShareWith
from apps.stockshare.serializers import ShareWithSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ShareWithView(ModelViewSet):
    queryset = ShareWith.objects.all()
    serializer_class = ShareWithSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShareWith.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
