# api/urls.py

from django.urls import path
from .views import MatchResultListView, MatchResultDetailView

urlpatterns = [
    path('matches/', MatchResultListView.as_view(), name='matchresult-list'),
    path('matches/<str:id>/', MatchResultDetailView.as_view(), name='matchresult-detail'),
]
