from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.stockshare.models import ShareWith
from apps.users.models import User

class ShareWithSerializer(ModelSerializer):
    shared_user = serializers.CharField() 
    class Meta:
        model = ShareWith
        fields = ["shared_user"]

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

