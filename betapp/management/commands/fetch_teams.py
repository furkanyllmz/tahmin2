# your_app/management/commands/list_api_teams.py

import os
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Football-Data.org API’den bir competition’daki takımları listeler."

    def add_arguments(self, parser):
        parser.add_argument(
            '--competition', '-c',
            dest='competition_id',
            required=True,
            help="Competition ID (örneğin 2021=Premier League, 2014=La Liga, 2019=Serie A, 2002=Bundesliga, 2015=Ligue 1, 2017=Süper Lig)"
        )
        parser.add_argument(
            '--season', '-s',
            dest='season',
            type=int,
            help="(Opsiyonel) Sezon yılı (örn. 2023). V4 endpoint’de otomatik seçiliyor genelde."
        )

    def handle(self, *args, **options):
        API_KEY = "96bc313d869b43288a042b9d142f30f9"
        if not API_KEY:
            self.stderr.write("⚠️ Lütfen FOOTBALL_DATA_API_KEY environment değişkenini ayarlayın.")
            return

        comp_id = options['competition_id']
        season = options.get('season')

        url = f"https://api.football-data.org/v4/competitions/{comp_id}/teams"
        headers = {"X-Auth-Token": API_KEY}
        params = {}
        if season:
            params['season'] = season

        self.stdout.write(f"🔍 Competition {comp_id} takımları çekiliyor…")
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            self.stderr.write(f"❌ API hatası ({r.status_code}): {r.text}")
            return

        data = r.json()
        teams = data.get('teams', [])
        if not teams:
            self.stdout.write("⚠️ Hiç takım bulunamadı.")
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Toplam {len(teams)} takım bulundu:"))
        for t in teams:
            name = t.get('name')
              
            
            self.stdout.write(f"\"{name}\":\" \",")
