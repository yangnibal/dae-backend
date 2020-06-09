from .models import Score, Logo
from rest_framework import serializers

class ScoreSerializer(serializers.ModelSerializer):
    percent = serializers.CharField(read_only=True)
    rank = serializers.CharField(read_only=True)
    rating = serializers.CharField(read_only=True)
    test = serializers.CharField(source='test.id', read_only=True)
    student = serializers.CharField(source='student.name', read_only=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    z = serializers.CharField(read_only=True)
    prob_dens = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Score
        fields = ['score', 'percent', 'rank', 'rating', 'test', 'student', 'owner', 'z', 'prob_dens', 'id']

    def update(self, instance, validate_data):
        instance.score = validate_data.get("score", instance.score)

        instance.save()
        return instance

class LogoSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(use_url=True)
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Logo
        fields = ['owner', 'logo']