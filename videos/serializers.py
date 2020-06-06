from .models import Video
from rest_framework import serializers

class VideoSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name', read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Video
        fields = ['name', 'link', 'iframe', 'subject', 'grade', 'group', 'id']

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.link = validate_data.get("link", instance.link)
        instance.iframe = validate_data.get("iframe", instance.iframe)
        instance.subject = validate_data.get("subject", instance.subject)
        instance.grade = validate_data.get("grade", instance.grade)

        instance.save()
        return instance