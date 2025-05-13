from django.core.management.base import BaseCommand
from django.utils import timezone
from matches.models import PastMatches, MatchResult

class Command(BaseCommand):
    help = 'Bugünden önceki PastMatches skorlarını MatchResult tablosuna yazar.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        self.stdout.write(f"▶️ {today} öncesi tüm PastMatches skorları güncelleniyor…")

        # Bugünden önceki tüm maçlar
        pms = PastMatches.objects.filter(date__lt=today)
        updated_count = 0

        for pm in pms:
            rows = MatchResult.objects.filter(
                home_team=pm.home_team,
                away_team=pm.away_team,
                date=pm.date,
                league=pm.league
            ).update(
                ft_homegoals=pm.home_team_goal_count,
                ft_awaygoals=pm.away_team_goal_count
            )

            if rows:
                updated_count += rows
                self.stdout.write(
                    f"  ✓ {pm.date} | {pm.home_team} vs {pm.away_team} "
                    f"=> {pm.home_team_goal_count}-{pm.away_team_goal_count}"
                )

        self.stdout.write(f"\n✅ Toplam güncellenen satır: {updated_count}")
