from .models import Score
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