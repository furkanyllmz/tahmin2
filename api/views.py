from django.shortcuts import render

# api/views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView
from matches.models import MatchResult
from .serializers import MatchResultSerializer

class MatchResultListView(ListAPIView):
    serializer_class = MatchResultSerializer

    def get_queryset(self):
        qs = MatchResult.objects.all()
        date_str = self.request.query_params.get('date')  # "YYYY-MM-DD"
        if date_str:
            qs = qs.filter(date=date_str)  # <-- "date" kolonunuzun ismi bu mu?
        return qs

class MatchResultDetailView(RetrieveAPIView):
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer
    lookup_field = 'id'  # URL'deki <int:id> parametresini kullanacağız

