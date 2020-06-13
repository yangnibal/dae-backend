from .models import Material
from rest_framework import serializers

class MaterialSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="group.name", read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Material
        fields = ['name', 'link', 'subject', 'grade', 'group', 'id']

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.link = validate_data.get("link", instance.link)
        instance.subject = validate_data.get("subject", instance.subject)
        instance.grade = validate_data.get("grade", instance.grade)
        instance.group = validate_data.get("group", instance.group)

        instance.save()
        return instance