from .models import Test
from rest_framework import serializers

class TestSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", required=False)
    class Meta:
        model = Test
        fields = ['owner', 'grade', 'test_type', 'subject', 'average', 'std_dev', 'cand_num', 'additional_info', 'student', 'id']
    
    def update(self, instance, validate_data):
        instance.grade = validate_data.get("grade", instance.grade)
        instance.test_type = validate_data.get("test_type", instance.test_type)
        instance.subject = validate_data.get("subject", instance.subject)
        instance.average = validate_data.get("average", instance.average)
        instance.std_dev = validate_data.get("std_dev", instance.std_dev)
        instance.cand_num = validate_data.get("cand_num", instance.cand_num)
        instance.additional_info = validate_data.get("additional_info", instance.additional_info)
        instance.id = validate_data.get("id", instance.id)

        instance.save()
        return instance
