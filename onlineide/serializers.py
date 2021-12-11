from rest_framework import serializers
from .models import SubmissionCode
from django.contrib.auth.models import User


# removed because we are using knox
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubmissionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionCode
        fields = "__all__"

