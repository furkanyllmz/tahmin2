# matches/management/commands/print_globalteams.py

from django.core.management.base import BaseCommand
from collections import defaultdict
from matches.models import GlobalTeam

class Command(BaseCommand):
    help = "GlobalTeam tablosundaki tüm takım isimlerini lig bazında gruplayarak yazdırır."

    def handle(self, *args, **options):
        # Önce tüm kayıtları çekelim
        teams = GlobalTeam.objects.all().values('country', 'team_name')
        if not teams:
            self.stdout.write("⚠️ GlobalTeam tablosunda hiç kayıt yok.")
            return

        # "league" değerine göre grupla
        by_league = defaultdict(list)
        for entry in teams:
            league = entry['country'] or 'Unknown'
            by_league[league].append(entry['team_name'])

        # Yazdır
        for league, names in sorted(by_league.items()):
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== {league.upper()} ({len(names)}) ==="))
            for name in sorted(names):
                self.stdout.write(f" • {name}")
