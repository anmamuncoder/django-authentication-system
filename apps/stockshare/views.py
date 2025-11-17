from django.shortcuts import render
from rest_framework.views import APIView
from apps.stockshare.models import ShareWith
from apps.stockshare.serializers import ShareWithSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class ShareWithView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        serializer = ShareWithSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "connected!"}, status=201)

        