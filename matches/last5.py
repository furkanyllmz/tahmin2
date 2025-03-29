from datetime import date,timedelta
from django.db.models import Q
from matches.models import PastMatches  # PastMatches modelini kullanıyoruz

def get_last5(league, team_name):
    """
    Verilen takımın (ev veya deplasman) bugüne kadar oynadığı maçlardan,
    en güncel 5 maçın bilgilerini döndürür.
    Eğer league parametresi verilmişse, onu da filtreye ekler.
    """
    today = date.today()- timedelta(days=1)
    qs = PastMatches.objects.filter(
        Q(home_team__iexact=team_name) | Q(away_team__iexact=team_name),
        date__lte=today  # Bugüne kadar oynanmış maçlar
    )
    if league:
        qs = qs.filter(league__iexact=league)
    qs = qs.order_by('-date')[:5]  # En güncel 5 maç
    last5 = []
    for match in qs:
        score = f"{match.home_team_goal_count}-{match.away_team_goal_count}"
        last5.append({
            "home_team_name": match.home_team,
            "away_team_name": match.away_team,
            "score": score,
            "date": match.date
        })
    return last5
