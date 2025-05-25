# from rest_framework import serializers
# from .models import Lead, ActivityLog
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class LeadSerializer(serializers.ModelSerializer):
#     assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
#
#     class Meta:
#         model = Lead
#         fields = '__all__'
#
# class ActivityLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ActivityLog
#         fields = '__all__'
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'role', 'department']
#
from rest_framework import serializers
from .models import Lead, ActivityLog
from django.contrib.auth import get_user_model

User = get_user_model()

# Lead Serializer
class LeadSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model = Lead
        fields = '__all__'

# Activity Log Serializer
class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

# Basic User Serializer (for fetching user data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'department']

# Register Serializer (for user registration)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
