# your_app/management/commands/today_to_tomorrow_finished_matches.py

import os
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Football-Data.org API’den bugünden yarına kadar sonuçlanan maçları çeker."

    def handle(self, *args, **options):
        API_KEY = "96bc313d869b43288a042b9d142f30f9"
        if not API_KEY:
            self.stderr.write("❌ Lütfen FOOTBALL_DATA_API_KEY env değişkenini ayarlayın.")
            return

        # Bugün ve yarın ISO formatında
        today   = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        yesterday=today + timedelta(days=-1)

        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": API_KEY}
        params = {
            "dateFrom": yesterday.isoformat(),
            "dateTo":   tomorrow.isoformat(),
            "status":   "FINISHED"
        }

        self.stdout.write(f"🔍 {params['dateFrom']} → {params['dateTo']} arasında FINISHED statüsündeki maçlar çekiliyor…")
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            self.stderr.write(f"❌ API Hatası ({resp.status_code}): {resp.text}")
            return

        matches = resp.json().get("matches", [])
        if not matches:
            self.stdout.write("⚠️ İlgili tarihler arasında bitmiş maç bulunamadı.")
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Toplam {len(matches)} maç bulundu:"))
        for m in matches:
            home    = m["homeTeam"]["name"]
            away    = m["awayTeam"]["name"]
            score_h = m["score"]["fullTime"]["home"]
            score_a = m["score"]["fullTime"]["away"]
            comp    = m["competition"]["name"]
            kickoff = m["utcDate"]
            self.stdout.write(f" • [{comp}] {home} {score_h}-{score_a} {away}  ({kickoff})")
