from apps.inventory.models import Category,Inventory
from rest_framework.serializers import Serializer,ModelSerializer, ValidationError,SerializerMethodField
# --------------------------
# Category Serializer
# --------------------------
class CategorySerializer(ModelSerializer):
    total_inventory = SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_total_inventory(self, obj):
        return obj.inventory_count
    
    def validate_name(self, value):
        user = self.context['user']
        if Category.objects.filter(user=user, name=value).exists():
            raise ValidationError("Category with this name already exists.")
        return value
    
    def create(self, validated_data):
        user = self.context['user']
        validated_data.pop('user', None) 
        return Category.objects.create(user=user,**validated_data)

# --------------------------
# Inventory Serializer
# --------------------------
class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__' 