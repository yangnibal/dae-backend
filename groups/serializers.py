from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Group
        fields = ['name', 'owner']