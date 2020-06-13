from rest_framework import serializers
from .models import InfGroup, Group

class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Group
        fields = ['name', 'owner', 'id']

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)

        instance.save()
        return instance


class InfGroupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = InfGroup
        fields = ['name', 'id']

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)

        instance.save()
        return instance