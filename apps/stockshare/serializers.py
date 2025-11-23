from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.stockshare.models import ShareWith
from apps.inventory.models import Inventory
from apps.users.models import User

class ShareWithSerializer(ModelSerializer):
    shared_user = serializers.CharField() 

    class Meta:
        model = ShareWith
        fields = ['id',"shared_user",'created_at']
        read_only_fields = ['id','created_at']
    
    def validate(self, attrs):
        request = self.context['request']
        user1 = request.user 
        try:
            user2 = User.objects.get(username=attrs["shared_user"] )
        except User.DoesNotExist:
            raise serializers.ValidationError({"shared_user": "User not found"})
        if user1 == user2:
            raise serializers.ValidationError("You cannot share with yourself.")
 
        attrs["user2"] = user2  
        return attrs
    
    def create(self, validated_data):
        user1 = self.context["request"].user
        user2 = validated_data["user2"]
 
        ShareWith.objects.get_or_create(owner=user1, shared_user=user2)
        ShareWith.objects.get_or_create(owner=user2, shared_user=user1)

        return validated_data

# --------------------------
# Inventory Serializer ( for WebSocket )
# --------------------------
# UUIDs are converted to strings safely.
class InventorySerializerUUIDtoSTRING(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    category = serializers.UUIDField(source='category.name',read_only=True)
    user = serializers.UUIDField(source='user.username', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'priority','number','category', 'user','created_at']  # include id safely

    # id = serializers.UUIDField(format='hex', read_only=True)        # Convert UUID to string
    # 123e4567-e89b-12d3-a456-426614174000 -> 123e4567e89b12d3a456426614174000
