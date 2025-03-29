import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from models import PastMatches
from dateconvert import parse_date_only  # "Feb 25 2025 - 12:00pm" -> "2025-02-25"
import numpy as np
import pandas as pd
from matches.dateconvert import parse_date_only
from matches.dateconvert import get_time
from models import PastMatches
from pathlib import Path
from django.core.management.base import BaseCommand

def load_global_matches():
    BASE_DIR = Path(__file__).resolve().parent  # Örneğin, betmodel dizini
    DATA_FOLDER = BASE_DIR / "betmodel/stats"
    files = os.listdir(DATA_FOLDER)
    # "matches" içeren CSV dosyalarını alalım:
    matches_files = [f for f in files if "matches" in f.lower() and f.endswith(".csv")]
    
    for file in matches_files:
        file_path = os.path.join(DATA_FOLDER, file)
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        df.columns = df.columns.str.strip()
        # Lig bilgisini dosya adından veya CSV'den alabilirsiniz.
        # Örneğin, dosya adından "turkiye-superlig-matches.csv" -> "Türkiye Süper Lig"
        league = file.split("-")[0].capitalize()  # basit örnek
        
        for _, row in df.iterrows():
            # CSV'deki date_GMT sütununu parse_date_only ile ISO formata çevirin
            date_str = parse_date_only(row["date_GMT"])  # Örneğin: "2025-02-25"
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue  # Tarih parse edilemezse atla
            
            # Zaman bilgisi, CSV'de farklı formatta olabilir; isteğe bağlı parse edilebilir.
            # Örneğin, "12:00pm" stringini 24 saatlik formata çevirmek.
            # Burada basitçe row["time"] kullanıyoruz.
            time_str = row.get("time", "00:00")
            try:
                time_obj = datetime.strptime(time_str, "%I:%M%p").time()
            except ValueError:
                time_obj = None

            # GlobalMatch modelinde veriyi update_or_create ile ekleyin:
            PastMatches.objects.update_or_create(
                league=league,
                home_team=row["home_team_name"],
                away_team=row["away_team_name"],
                date=date_obj,
                home_team_goal_count = row["home_team_goal_count"],
                away_team_goal_count = row["away_team_goal_count"],
                home_team_goal_count_half_time = row["home_team_goal_count_half_time"],
                away_team_goal_count_half_time = row["away_team_goal_count_half_time"],
                home_team_corner_count = row["home_team_corner_count"],
                away_team_corner_count = row["away_team_corner_count"],
                home_team_yellow_cards = row["home_team_yellow_cards"],
                home_team_red_cards = row["home_team_red_cards"],
                away_team_yellow_cards = row["away_team_yellow_cards"],
                away_team_red_cards = row["away_team_red_cards"],
                home_team_first_half_cards = row["home_team_first_half_cards"],
                home_team_second_half_cards = row["home_team_second_half_cards"],
                away_team_first_half_cards = row["away_team_first_half_cards"],
                away_team_second_half_cards = row["away_team_second_half_cards"],
                home_team_shots = row["home_team_shots"],
                away_team_shots = row["away_team_shots"],
                home_team_shots_on_target = row["home_team_shots_on_target"],
                away_team_shots_on_target = row["away_team_shots_on_target"],
                home_team_possession = row["home_team_possession"],
                away_team_possession = row["away_team_possession"],
                away_team_pre_match_xG = row["Away Team Pre-Match xG"],
                team_a_xg = row["team_a_xg"],
                team_b_xg = row["team_b_xg"],

            )
