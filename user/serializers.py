from rest_framework import serializers
from .models import Profile, CustomUser
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validate the password and password confirmation fields match
        """
        password = data.get('password')
        confirm_password = data.pop('confirm_password', None)

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        """ Create a new user """
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CusomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = CusomUserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
