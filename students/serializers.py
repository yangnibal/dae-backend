from .models import Student
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    group = serializers.CharField(source='group.name', read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Student
        fields = ['name', 'grade', 'group', 'owner', 'id']

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.grade = validate_data.get("grade", instance.grade)
        instance.group = validate_data.get("group", instance.group)

        instance.save()
        return instance