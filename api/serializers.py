# api/serializers.py

from rest_framework import serializers
from matches.models import MatchResult  # Sizin tahmin sonuç modeliniz

class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchResult
        fields = '__all__'  # Tüm alanları JSON olarak döndür
        # veya fields = ["id", "home_team", "away_team", "ms1", "msx", "ms2", "date", ...]
