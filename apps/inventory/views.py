from django.shortcuts import render
# Create your views here.
from apps.inventory.models import Category,Inventory
from apps.inventory.serializers import CategorySerializer,InventorySerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# --------------------------
# Category View
# --------------------------
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        user = request.user
        cat_id = kwargs.get('id')
        if cat_id:
            # category = Category.objects.get(id=cat_id,user=user)
            category = get_object_or_404(Category,id=cat_id,user=user) # for safety
            serializer = CategorySerializer(category) 
        else:
            category = Category.objects.filter(user=user)
            serializer = CategorySerializer(category,many=True) 
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = CategorySerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def put(self,request,*args,**kwargs):
        return self.custome_update(request,*args,**kwargs)
    
    def patch(self,request,*args,**kwargs):
        return self.custome_update(request,*args,**kwargs)

    # PUT & PATCH Method same, if any category using in Inventory so cant edit and delete
    def custome_update(self,request,*args,**kwargs):
        cat_id = kwargs.get('id')
        cat = get_object_or_404(Category,id=cat_id,user=request.user)

        if cat.inventory_count > 0:
            return Response({'detail':f"This Category already useing {cat.inventory_count}, You can't edit!"},status=status.HTTP_403_FORBIDDEN)
        
        serializer = CategorySerializer(cat,data=request.data,partial=True,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,*args,**kwargs):
        cat_id = kwargs.get('id')
        cat = get_object_or_404(Category,id=cat_id,user=request.user)
        if cat.inventory_count > 0:
            return Response({'detail':f"This Category already useing {cat.inventory_count}, You can't delete that!"},status=status.HTTP_403_FORBIDDEN)
        
        cat.delete()
        return Response({'detail': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

# --------------------------
# Inventory View  : 
# --------------------------
class InventoryView(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
 