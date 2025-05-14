# your_app/management/commands/update_finished_scores.py

import os
import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from matches.models import MatchResult

class Command(BaseCommand):
    help = "Football-Data.org’dan önceki günlerden yarına kadar FINISHED maçları çekip, DB’deki skorları günceller."

    # Buraya API takım isimlerini, kendi DB'nizdeki karşılık gelen isimlerle eşleyin
    NAME_MAPPING = {
        "Toulouse FC":"Toulouse",
        "Stade Brestois 29":"Brest",
        "Olympique de Marseille":"Olympique Marseille",
        "Montpellier HSC":"Montpellier",
        "AJ Auxerre":"Auxerre",
        "Lille OSC":"Lille",
        "OGC Nice":"Nice ",
        "Olympique Lyonnais":"Olympique Lyonnais",
        "Paris Saint-Germain FC":"PSG",
        "AS Saint-Étienne":"Saint-Étienne",
        "Stade Rennais FC 1901":"Rennes",
        "Angers SCO":"Angers SCO",
        "Le Havre AC":"Le Havre",
        "FC Nantes":"Nantes",
        "Racing Club de Lens":"Lens",
        "Stade de Reims":"Reims",
        "AS Monaco FC":"Monaco",
        "RC Strasbourg Alsace":"Strasbourg",

        "Athletic Club":"Athletic Club Bilbao",
        "Club Atlético de Madrid":"Atlético Madrid",
        "CA Osasuna":"CA Osasuna",
        "RCD Espanyol de Barcelona":"RCD Espanyol",
        "FC Barcelona":"FC Barcelona",
        "Getafe CF":"Getafe CF",
        "Real Madrid CF":"Real Madrid",
        "Rayo Vallecano de Madrid":"Rayo Vallecano",
        "RCD Mallorca":"RCD Mallorca",
        "Real Betis Balompié":"Real Betis",
        "Real Sociedad de Fútbol":"Real Sociedad",
        "Villarreal CF":"Villarreal",
        "Valencia CF":"Valencia CF",
        "Real Valladolid CF":"Real Valladolid",
        "Deportivo Alavés":"Deportivo Alavés",
        "UD Las Palmas":"UD Las Palmas",
        "Girona FC":"Girona FC",
        "RC Celta de Vigo":"Celta de Vigo",
        "Sevilla FC":"Sevilla FC",
        "CD Leganés":"Leganés",

        "AC Milan":"AC Milan",
        "ACF Fiorentina":"Fiorentina",
        "AS Roma":"Roma",
        "Atalanta BC":"Atalanta",
        "Bologna FC 1909":"Bologna",
        "Cagliari Calcio":"Cagliari",
        "Genoa CFC":"Genoa",
        "FC Internazionale Milano":"Inter Milan",
        "Juventus FC":"Juventus",
        "SS Lazio":"Lazio",
        "Parma Calcio 1913":"Parma",
        "SSC Napoli":"Napoli",
        "Udinese Calcio":"Udinese",
        "Empoli FC":"Empoli",
        "Hellas Verona FC":"Hellas Verona",
        "Venezia FC":"Venezia",
        "Torino FC":"Torino",
        "US Lecce":"Lecce",
        "AC Monza":"Monza",
        "Como 1907":"Como",

        "Rio Ave FC":" Rio Ave FC ",
        "Sporting Clube de Portugal":" Sporting CP ",
        "FC Porto":"Porto",
        "GD Estoril Praia":" GD Estoril Praia ",
        "Moreirense FC":" Moreirense FC ",
        "FC Arouca":" FC Arouca ",
        "Boavista FC":" Boavista FC ",
        "Sport Lisboa e Benfica":" Benfica ",
        "CD Nacional":" CD Nacional ",
        "CD Santa Clara":" Santa Clara ",
        "FC Famalicão":" Famalicão ",
        "Gil Vicente FC":" Gil Vicente ",
        "Vitória SC":" Vitória Guimarães ",
        "SC Farense":" Farense ",
        "Sporting Clube de Braga":" Sporting Braga ",
        "Casa Pia AC":" Casa Pia ",
        "CF Estrela da Amadora":" Estrela Amadora ",
        "AVS":" AVS ",

        

        "Arsenal FC": "Arsenal",
        "Aston Villa FC": "Aston Villa",
        "Chelsea FC": "Chelsea",
        "Everton FC": "Everton",
        "Fulham FC": "Fulham",
        "Liverpool FC": "Liverpool",
        "Manchester City FC": "Manchester City",
        "Manchester United FC": "Manchester United",
        "Newcastle United FC": "Newcastle United",
        "Tottenham Hotspur FC": "Tottenham Hotspur",
        "Wolverhampton Wanderers FC": "Wolverhampton Wanderers",
        "Leicester City FC": "Leicester City",
        "Southampton FC": "Southampton",
        "Ipswich Town FC": "Ipswich Town",
        "Nottingham Forest FC": "Nottingham Forest",
        "Crystal Palace FC": "Crystal Palace",
        "Brighton & Hove Albion FC": "Brighton & Hove Albion",
        "Brentford FC": "Brentford",
        "West Ham United FC": "West Ham United",
        "AFC Bournemouth": "AFC Bournemouth",
        "FC Twente '65": "Twente",
        "Heracles Almelo": "Heracles",
        "Willem II Tilburg": "Willem II",
        "SC Heerenveen": "Heerenveen",
        "PSV": "PSV",
        "Feyenoord Rotterdam": "Feyenoord",
        "FC Utrecht": "Utrecht",
        "FC Groningen": "Groningen",
        "AFC Ajax": "Ajax",
        "NAC Breda": "NAC Breda",
        "AZ": "AZ",
        "RKC Waalwijk": "RKC Waalwijk",
        "PEC Zwolle": "PEC Zwolle",
        "Go Ahead Eagles": "Go Ahead Eagles",
        "Almere City FC": "Almere City",
        "NEC": "NEC",
        "Fortuna Sittard": "Fortuna Sittard",
        "Sparta Rotterdam": "Sparta Rotterdam"


        # …
    }

    def handle(self, *args, **options):
        API_KEY = "96bc313d869b43288a042b9d142f30f9"
        if not API_KEY:
            return self.stderr.write("❌ Lütfen FOOTBALL_DATA_API_KEY ayarlayın.")

        today     = datetime.utcnow().date()
        tomorrow  = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": API_KEY}
        params = {
            "dateFrom": today.isoformat(),
            "dateTo":   tomorrow.isoformat(),
            "status":   "FINISHED"
        }

        self.stdout.write(f"🔍 {params['dateFrom']} → {params['dateTo']} arasında FINISHED maçlar çekiliyor…")
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            return self.stderr.write(f"❌ API Hatası ({resp.status_code}): {resp.text}")

        matches = resp.json().get("matches", [])
        if not matches:
            return self.stdout.write("⚠️ Bu aralıkta bitmiş maç yok.")

        updated = 0
        for m in matches:
            # API’den gelen isimler
            api_home = m["homeTeam"]["name"]
            api_away = m["awayTeam"]["name"]
            # Map edip DB isimlerini al
            home     = self.NAME_MAPPING.get(api_home, api_home)
            away     = self.NAME_MAPPING.get(api_away, api_away)

            # Skor
            score_h = m["score"]["fullTime"]["home"]
            score_a = m["score"]["fullTime"]["away"]
            # Lig ve tarih
            comp     = m["competition"]["name"]
            match_dt = m["utcDate"][:10]  # "YYYY-MM-DD"

            # DB’deki eşleşmeyi bul ve güncelle
            qs = MatchResult.objects.filter(
                home_team=home,
                away_team=away,
                date=match_dt,
                ft_homegoals__isnull=True,
                ft_awaygoals__isnull=True,
                
            )
            print(api_home)
            if qs.exists():
                qs.update(ft_homegoals=score_h, ft_awaygoals=score_a)
                updated += qs.count()
                self.stdout.write(f"✓ Güncellendi: {home} {score_h}-{score_a} {away} ({match_dt})")
            else:
                self.stdout.write(f"• Eşleşme bulunamadı: {home} vs {away} ({match_dt}) in {comp}")

        self.stdout.write(self.style.SUCCESS(f"\nToplam güncellenen maç: {updated}"))
