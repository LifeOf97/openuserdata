# from rest_framework.validators import UniqueTogetherValidator
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from . import models

# Custom user model
User = get_user_model()


class APIRootSerializer(serializers.Serializer):
    hello = serializers.CharField()
    home_page = serializers.CharField()
    documentations = serializers.JSONField()


class CreatorsOpenUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'app_name', 'uid', 'cid', 'aid', 'username', 'email',
            'first_name', 'last_name', 'other_name',
            'mugshot', 'gender', 'dob', 'about', "password"
        )
        extra_kwargs = {
            'app_name': {'read_only': True},
            'password': {'write_only': True},
            'uid': {'read_only': True}
        }

    def to_internal_value(self, data):
        if data.get('username'):
            data['username'] = data['username'].replace(' ', '_').lower()
        if data.get('gender'):
            data['gender'] = str(data['gender']).capitalize()
        return super().to_internal_value(data)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.other_name = validated_data.get('other_name', instance.other_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.mugshot = validated_data.get('mugshot', instance.mugshot)
        instance.about = validated_data.get('about', instance.about)

        instance.save()
        return instance


class OpenUserDataserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uid', 'username', 'email',
            'first_name', 'last_name', 'other_name',
            'mugshot', 'gender', 'dob', 'about'
        )


class LoginSessionSerializer(serializers.Serializer):
    """
    Login serializer to facilitate the session authentication
    """
    username = serializers.CharField()
    password = serializers.CharField()
