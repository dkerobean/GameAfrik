from rest_framework import serializers
from .models import Profile, CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def validate(self, data):
            """
            Validate the password and password confirmation fields match
            """

            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if password and confirm_password and password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")

            return data

        def create(self, validated_data):
            """ Create a new user """

            user = CustomUser.objects.create(
                name=validated_data['name'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user


class CusomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = CusomUserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
