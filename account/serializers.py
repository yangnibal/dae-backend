from rest_framework import serializers
from .models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'name', 'is_staff', 'password', 'phone_number', 'email', 'can_access_1', 'can_access_2', 'id']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.can_access_1 = validated_data.get("can_access_1", instance.can_access_1)
        instance.can_access_2 = validated_data.get("can_access_2", instance.can_access_2)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')


        attrs['user'] = user
        return attrs