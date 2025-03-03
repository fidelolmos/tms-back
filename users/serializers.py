from rest_framework import serializers
from .models import CustomUser, UserRoles

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', UserRoles.DRIVER)
        user = CustomUser.objects.create_user(**validated_data, role=role)
        return user
