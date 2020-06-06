from rest_framework import serializers
from .models import InfGroup, Group

class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Group
        fields = ['name', 'owner']

class InfGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfGroup
        fields = ['name']