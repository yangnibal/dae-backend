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

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)

        instance.save()
        return instance