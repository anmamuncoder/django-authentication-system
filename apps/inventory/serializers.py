from apps.inventory.models import Category,Inventory
from rest_framework.serializers import Serializer,ModelSerializer

# --------------------------
# Category Serializer
# --------------------------
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['user'] 
        return Category.objects.create(user=user,**validated_data)

# --------------------------
# Inventory Serializer
# --------------------------
class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__' 

