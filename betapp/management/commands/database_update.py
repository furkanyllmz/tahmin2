# betapp/management/commands/database_update.py

from django.core.management.base import BaseCommand
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from matches.dateconvert import parse_date_only,get_time
from matches.models import PastMatches,GlobalTeam
from django.db import transaction

class Command(BaseCommand):
    help = "CSV dosyalarından verileri okuyup, PastMatches modelini günceller."

    def handle(self, *args, **options):
        self.stdout.write("Maç verileri güncelleniyor...")
        self.update_matches()
        self.stdout.write(self.style.SUCCESS("Maç verileri başarıyla güncellendi."))

        self.stdout.write("Global takım verileri güncelleniyor...")
        with transaction.atomic():
            self.update_global_teams()
        self.stdout.write(self.style.SUCCESS("Global takım verileri başarıyla güncellendi."))
        
        
        
    def update_matches(self):    
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        DATA_FOLDER = BASE_DIR / "matches" / "betmodel" / "stats"
        files = os.listdir(DATA_FOLDER)
        matches_files = [f for f in files if "matches" in f.lower() and f.endswith(".csv")]
        for file in matches_files:
            file_path = os.path.join(DATA_FOLDER, file)
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()
            country = file.split("-")[0].capitalize()
            print(country)
            league=file.split("matches")[0].rstrip("-").strip()  
            print(league)
        


            for _, row in df.iterrows():
                date_str = parse_date_only(row["date_GMT"])
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue

                time_str = row.get("time", "00:00")
                try:
                    time_obj = datetime.strptime(time_str, "%I:%M%p").time()
                except ValueError:
                    time_obj = None
                # Örnek olarak update_or_create ile veriyi güncelliyoruz.
                with transaction.atomic():
                    PastMatches.objects.update_or_create(
                        league=league,
                        country=country,
                        home_team=row["home_team_name"],
                        away_team=row["away_team_name"],
                        date=parse_date_only(row["date_GMT"]),
                        time=get_time(row["date_GMT"]),
                        defaults={
                            "home_team_goal_count": row["home_team_goal_count"],
                            "away_team_goal_count": row["away_team_goal_count"],
                            "home_team_goal_count_half_time": row["home_team_goal_count_half_time"],
                            "away_team_goal_count_half_time": row["away_team_goal_count_half_time"],
                            "home_team_corner_count": row["home_team_corner_count"],
                            "away_team_corner_count": row["away_team_corner_count"],
                            "home_team_yellow_cards": row["home_team_yellow_cards"],
                            "home_team_red_cards": row["home_team_red_cards"],
                            "away_team_yellow_cards": row["away_team_yellow_cards"],
                            "away_team_red_cards": row["away_team_red_cards"],
                            "home_team_first_half_cards": row["home_team_first_half_cards"],
                            "home_team_second_half_cards": row["home_team_second_half_cards"],
                            "away_team_first_half_cards": row["away_team_first_half_cards"],
                            "away_team_second_half_cards": row["away_team_second_half_cards"],
                            "home_team_shots": row["home_team_shots"],
                            "away_team_shots": row["away_team_shots"],
                            "home_team_shots_on_target": row["home_team_shots_on_target"],
                            "away_team_shots_on_target": row["away_team_shots_on_target"],
                            "home_team_possession": row["home_team_possession"],
                            "away_team_possession": row["away_team_possession"],
                            "team_a_xg": row["team_a_xg"],
                            "team_b_xg": row["team_b_xg"],
                        }
                    )

            self.stdout.write(self.style.SUCCESS("Maç verileri başarıyla güncellendi."))
    def update_global_teams(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        DATA_FOLDER = BASE_DIR / "matches" / "betmodel" / "stats"
        files = os.listdir(DATA_FOLDER)
        teams_files = [f for f in files if "teams" in f.lower() and f.endswith(".csv")]
        
        global_data = {}
        for file in teams_files:
            file_path = os.path.join(DATA_FOLDER, file)
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()
            # Örnek: dosya adı "turkiye-superlig-teams.csv" -> lig: "Türkiye Süper Lig"
            league = file.split("-")[0].capitalize()
            
            
            for _, row in df.iterrows():
                team = row["common_name"]
                key = team
                if league== "International":
                    country=league
                else:    
                    country = row["country"] if "country" in row and not pd.isna(row["country"]) else "abc"

                matches_played=row["matches_played"] if not pd.isna(row["matches_played"]) else 0
                wins = int(row["wins"]) if not pd.isna(row["wins"]) else 0
                wins_home = int(row["wins_home"]) if not pd.isna(row["wins_home"]) else 0
                wins_away = int(row["wins_away"]) if not pd.isna(row["wins_away"]) else 0
                draws = int(row["draws"]) if not pd.isna(row["draws"]) else 0
                draws_home = int(row["draws_home"]) if not pd.isna(row["draws_home"]) else 0
                draws_away = int(row["draws_away"]) if not pd.isna(row["draws_away"]) else 0
                losses = int(row["losses"]) if not pd.isna(row["losses"]) else 0
                losses_home = int(row["losses_home"]) if not pd.isna(row["losses_home"]) else 0
                losses_away = int(row["losses_away"]) if not pd.isna(row["losses_away"]) else 0
                goals_scored = int(row["goals_scored"]) if not pd.isna(row["goals_scored"]) else 0
                goals_scored_home = int(row["goals_scored_home"]) if not pd.isna(row["goals_scored_home"]) else 0
                goals_scored_away = int(row["goals_scored_away"]) if not pd.isna(row["goals_scored_away"]) else 0
                corners_total = row["corners_total"] if not pd.isna(row["corners_total"]) else 0
                corners_total_home = row["corners_total_home"] if not pd.isna(row["corners_total_home"]) else 0
                corners_total_away = row["corners_total_away"] if not pd.isna(row["corners_total_away"]) else 0
                cards_total = row["cards_total"] if not pd.isna(row["cards_total"]) else 0
                cards_total_home = row["cards_total_home"] if not pd.isna(row["cards_total_home"]) else 0
                cards_total_away = row["cards_total_away"] if not pd.isna(row["cards_total_away"]) else 0
                average_possession = row["average_possession"] if not pd.isna(row["average_possession"]) else 0
                average_possession_home = row["average_possession_home"] if not pd.isna(row["average_possession_home"]) else 0
                average_possession_away = row["average_possession_away"] if not pd.isna(row["average_possession_away"]) else 0
                shots = row["shots"] if not pd.isna(row["shots"]) else 0
                shots_home = row["shots_home"] if not pd.isna(row["shots_home"]) else 0
                shots_away = row["shots_away"] if not pd.isna(row["shots_away"]) else 0
                shots_on_target = row["shots_on_target"] if not pd.isna(row["shots_on_target"]) else 0
                shots_on_target_home = row["shots_on_target_home"] if not pd.isna(row["shots_on_target_home"]) else 0
                shots_on_target_away = row["shots_on_target_away"] if not pd.isna(row["shots_on_target_away"]) else 0
                goals_scored_half_time = row["goals_scored_half_time"] if not pd.isna(row["goals_scored_half_time"]) else 0
                goals_scored_half_time_home = row["goals_scored_half_time_home"] if not pd.isna(row["goals_scored_half_time_home"]) else 0
                goals_scored_half_time_away = row["goals_scored_half_time_away"] if not pd.isna(row["goals_scored_half_time_away"]) else 0
                leading_at_half_time = row["leading_at_half_time"] if not pd.isna(row["leading_at_half_time"]) else 0
                leading_at_half_time_home = row["leading_at_half_time_home"] if not pd.isna(row["leading_at_half_time_home"]) else 0
                leading_at_half_time_away = row["leading_at_half_time_away"] if not pd.isna(row["leading_at_half_time_away"]) else 0
                draw_at_half_time = row["draw_at_half_time"] if not pd.isna(row["draw_at_half_time"]) else 0
                draw_at_half_time_home = row["draw_at_half_time_home"] if not pd.isna(row["draw_at_half_time_home"]) else 0
                draw_at_half_time_away = row["draw_at_half_time_away"] if not pd.isna(row["draw_at_half_time_away"]) else 0
                losing_at_half_time = row["losing_at_half_time"] if not pd.isna(row["losing_at_half_time"]) else 0
                losing_at_half_time_home = row["losing_at_half_time_home"] if not pd.isna(row["losing_at_half_time_home"]) else 0
                losing_at_half_time_away = row["losing_at_half_time_away"] if not pd.isna(row["losing_at_half_time_away"]) else 0
                over05_count = row["over05_count"] if not pd.isna(row["over05_count"]) else 0
                over15_count = row["over15_count"] if not pd.isna(row["over15_count"]) else 0
                over25_count = row["over25_count"] if not pd.isna(row["over25_count"]) else 0
                over35_count = row["over35_count"] if not pd.isna(row["over35_count"]) else 0
                over05_count_home = row["over05_count_home"] if not pd.isna(row["over05_count_home"]) else 0
                over15_count_home = row["over15_count_home"] if not pd.isna(row["over15_count_home"]) else 0
                over25_count_home = row["over25_count_home"] if not pd.isna(row["over25_count_home"]) else 0
                over35_count_home = row["over35_count_home"] if not pd.isna(row["over35_count_home"]) else 0
                over45_count_home = row["over45_count_home"] if not pd.isna(row["over45_count_home"]) else 0
                over55_count_home = row["over55_count_home"] if not pd.isna(row["over55_count_home"]) else 0
                over05_count_away = row["over05_count_away"] if not pd.isna(row["over05_count_away"]) else 0
                over15_count_away = row["over15_count_away"] if not pd.isna(row["over15_count_away"]) else 0
                over25_count_away = row["over25_count_away"] if not pd.isna(row["over25_count_away"]) else 0
                over35_count_away = row["over35_count_away"] if not pd.isna(row["over35_count_away"]) else 0
                over05_count_half_time = row["over05_count_half_time"] if not pd.isna(row["over05_count_half_time"]) else 0
                over15_count_half_time = row["over15_count_half_time"] if not pd.isna(row["over15_count_half_time"]) else 0
                over25_count_half_time = row["over25_count_half_time"] if not pd.isna(row["over25_count_half_time"]) else 0
                over05_count_half_time_home = row["over05_count_half_time_home"] if not pd.isna(row["over05_count_half_time_home"]) else 0
                over15_count_half_time_home = row["over15_count_half_time_home"] if not pd.isna(row["over15_count_half_time_home"]) else 0
                over25_count_half_time_home = row["over25_count_half_time_home"] if not pd.isna(row["over25_count_half_time_home"]) else 0
                over05_count_half_time_away = row["over05_count_half_time_away"] if not pd.isna(row["over05_count_half_time_away"]) else 0
                over15_count_half_time_away = row["over15_count_half_time_away"] if not pd.isna(row["over15_count_half_time_away"]) else 0
                over25_count_half_time_away = row["over25_count_half_time_away"] if not pd.isna(row["over25_count_half_time_away"]) else 0
                corners_per_match = row["corners_per_match"] if not pd.isna(row["corners_per_match"]) else 0
                corners_per_match_home = row["corners_per_match_home"] if not pd.isna(row["corners_per_match_home"]) else 0
                corners_per_match_away = row["corners_per_match_away"] if not pd.isna(row["corners_per_match_away"]) else 0
                cards_per_match = row["cards_per_match"] if not pd.isna(row["cards_per_match"]) else 0
                cards_per_match_home = row["cards_per_match_home"] if not pd.isna(row["cards_per_match_home"]) else 0
                cards_per_match_away = row["cards_per_match_away"] if not pd.isna(row["cards_per_match_away"]) else 0
                xg_for_avg_overall = row["xg_for_avg_overall"] if not pd.isna(row["xg_for_avg_overall"]) else 0
                xg_for_avg_home = row["xg_for_avg_home"] if not pd.isna(row["xg_for_avg_home"]) else 0
                xg_for_avg_away = row["xg_for_avg_away"] if not pd.isna(row["xg_for_avg_away"]) else 0
                xg_against_avg_overall = row["xg_against_avg_overall"] if not pd.isna(row["xg_against_avg_overall"]) else 0
                xg_against_avg_home = row["xg_against_avg_home"] if not pd.isna(row["xg_against_avg_home"]) else 0
                xg_against_avg_away = row["xg_against_avg_away"] if not pd.isna(row["xg_against_avg_away"]) else 0
                if key in global_data:
                    global_data[key]["country"] = country
                     
                    global_data[key]["wins"] += wins
                    global_data[key]["wins_home"] += wins_home
                    global_data[key]["wins_away"] += wins_away
                    global_data[key]["draws"] += draws
                    global_data[key]["draws_home"] += draws_home
                    global_data[key]["draws_away"] += draws_away
                    global_data[key]["losses"] += losses
                    global_data[key]["losses_home"] += losses_home
                    global_data[key]["losses_away"] += losses_away
                    global_data[key]["goals_scored"] += goals_scored
                    global_data[key]["goals_scored_home"] += goals_scored_home
                    global_data[key]["goals_scored_away"] += goals_scored_away
                    global_data[key]["corners_total"] += corners_total
                    global_data[key]["corners_total_home"] += corners_total_home
                    global_data[key]["corners_total_away"] += corners_total_away
                    global_data[key]["cards_total"] += 1
                    global_data[key]["cards_total_home"] += 1
                    global_data[key]["cards_total_away"] += 1
                    global_data[key]["shots"] += shots
                    global_data[key]["shots_home"] += shots_home
                    global_data[key]["shots_away"] += shots_away
                    global_data[key]["shots_on_target"] += shots_on_target
                    global_data[key]["shots_on_target_home"] += shots_on_target_home
                    global_data[key]["shots_on_target_away"] += shots_on_target_away
                    global_data[key]["goals_scored_half_time"] += goals_scored_half_time
                    global_data[key]["goals_scored_half_time_home"] += goals_scored_half_time_home
                    global_data[key]["goals_scored_half_time_away"] += goals_scored_half_time_away
                    global_data[key]["leading_at_half_time"] += leading_at_half_time
                    global_data[key]["leading_at_half_time_home"] += leading_at_half_time_home
                    global_data[key]["leading_at_half_time_away"] += leading_at_half_time_away
                    global_data[key]["draw_at_half_time"] += draw_at_half_time
                    global_data[key]["draw_at_half_time_home"] += draw_at_half_time_home
                    global_data[key]["draw_at_half_time_away"] += draw_at_half_time_away
                    global_data[key]["losing_at_half_time"] += losing_at_half_time
                    global_data[key]["losing_at_half_time_home"] += losing_at_half_time_home
                    global_data[key]["losing_at_half_time_away"] += losing_at_half_time_away
                    global_data[key]["over05_count"] += over05_count
                    global_data[key]["over15_count"] += over15_count
                    global_data[key]["over25_count"] += over25_count
                    global_data[key]["over35_count"] += over35_count
                    global_data[key]["over05_count_home"] += over05_count_home
                    global_data[key]["over15_count_home"] += over15_count_home
                    global_data[key]["over25_count_home"] += over25_count_home
                    global_data[key]["over35_count_home"] += over35_count_home
                    global_data[key]["over45_count_home"] += over45_count_home
                    global_data[key]["over55_count_home"] += over55_count_home
                    global_data[key]["over05_count_away"] += over05_count_away
                    global_data[key]["over15_count_away"] += over15_count_away
                    global_data[key]["over25_count_away"] += over25_count_away
                    global_data[key]["over35_count_away"] += over35_count_away
                    global_data[key]["over05_count_half_time"] += over05_count_half_time
                    global_data[key]["over15_count_half_time"] += over15_count_half_time
                    global_data[key]["over25_count_half_time"] += over25_count_half_time
                    global_data[key]["over05_count_half_time_home"] += over05_count_half_time_home
                    global_data[key]["over15_count_half_time_home"] += over15_count_half_time_home
                    global_data[key]["over25_count_half_time_home"] += over25_count_half_time_home
                    global_data[key]["over05_count_half_time_away"] += over05_count_half_time_away
                    global_data[key]["over15_count_half_time_away"] += over15_count_half_time_away
                    global_data[key]["over25_count_half_time_away"] += over25_count_half_time_away
                    global_data[key]["corners_per_match"] = (     (global_data[key]["corners_per_match"]*global_data[key]["matches_played"])  + (corners_per_match*matches_played))/(matches_played+global_data[key]["matches_played"])
                    global_data[key]["corners_per_match_home"] = ((global_data[key]["corners_per_match_home"]*global_data[key]["matches_played"])+ (corners_per_match_home*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["corners_per_match_away"] = ((global_data[key]["corners_per_match_away"]*global_data[key]["matches_played"])+ (corners_per_match_away*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["cards_per_match"] = ((global_data[key]["cards_per_match"]*global_data[key]["matches_played"])+ (cards_per_match*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["cards_per_match_home"] = ((global_data[key]["cards_per_match_home"]*global_data[key]["matches_played"])+ (cards_per_match_home*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["cards_per_match_away"] = ((global_data[key]["cards_per_match_away"]*global_data[key]["matches_played"])+ (cards_per_match_away*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_for_avg_overall"] = ((global_data[key]["xg_for_avg_overall"]*global_data[key]["matches_played"])+ (xg_for_avg_overall*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_for_avg_home"] = ((global_data[key]["xg_for_avg_home"]*global_data[key]["matches_played"])+ (xg_for_avg_home*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_for_avg_away"] = ((global_data[key]["xg_for_avg_away"]*global_data[key]["matches_played"])+ (xg_for_avg_away*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_against_avg_overall"] = ((global_data[key]["xg_against_avg_overall"]*global_data[key]["matches_played"])+ (xg_against_avg_overall*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_against_avg_home"] = ((global_data[key]["xg_against_avg_home"]*global_data[key]["matches_played"])+ (xg_against_avg_home*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["xg_against_avg_away"] = ((global_data[key]["xg_against_avg_away"]*global_data[key]["matches_played"])+ (xg_against_avg_away*matches_played))/ (matches_played+global_data[key]["matches_played"])
                    global_data[key]["matches_played"] +=matches_played
                    

                else:
                    global_data[key] = {
                        "country":country,
                        "wins": wins,
                        "wins_home": wins_home,
                        "wins_away": wins_away,
                        "draws": draws,
                        "draws_home": draws_home,
                        "draws_away": draws_away,
                        "losses": losses,
                        "losses_home": losses_home,
                        "losses_away": losses_away,
                        "goals_scored": goals_scored,
                        "goals_scored_home": goals_scored_home,
                        "goals_scored_away": goals_scored_away,
                        "corners_total": corners_total,
                        "corners_total_home": corners_total_home,
                        "corners_total_away": corners_total_away,
                        "cards_total": cards_total,
                        "cards_total_home": cards_total_home,
                        "cards_total_away": cards_total_away,
                        "average_possession": average_possession,
                        "average_possession_home": average_possession_home,
                        "average_possession_away": average_possession_away,
                        "shots": shots,
                        "shots_home": shots_home,
                        "shots_away": shots_away,
                        "shots_on_target": shots_on_target,
                        "shots_on_target_home": shots_on_target_home,
                        "shots_on_target_away": shots_on_target_away,
                        "goals_scored_half_time": goals_scored_half_time,
                        "goals_scored_half_time_home": goals_scored_half_time_home,
                        "goals_scored_half_time_away": goals_scored_half_time_away,
                        "leading_at_half_time": leading_at_half_time,
                        "leading_at_half_time_home": leading_at_half_time_home,
                        "leading_at_half_time_away": leading_at_half_time_away,
                        "draw_at_half_time": draw_at_half_time,
                        "draw_at_half_time_home": draw_at_half_time_home,
                        "draw_at_half_time_away": draw_at_half_time_away,
                        "losing_at_half_time": losing_at_half_time,
                        "losing_at_half_time_home": losing_at_half_time_home,
                        "losing_at_half_time_away": losing_at_half_time_away,
                        "over05_count": over05_count,
                        "over15_count": over15_count,
                        "over25_count": over25_count,
                        "over35_count": over35_count,
                        "over05_count_home": over05_count_home,
                        "over15_count_home": over15_count_home,
                        "over25_count_home": over25_count_home,
                        "over35_count_home": over35_count_home,
                        "over45_count_home": over45_count_home,
                        "over55_count_home": over55_count_home,
                        "over05_count_away": over05_count_away,
                        "over15_count_away": over15_count_away,
                        "over25_count_away": over25_count_away,
                        "over35_count_away": over35_count_away,
                        "over05_count_half_time": over05_count_half_time,
                        "over15_count_half_time": over15_count_half_time,
                        "over25_count_half_time": over25_count_half_time,
                        "over05_count_half_time_home": over05_count_half_time_home,
                        "over15_count_half_time_home": over15_count_half_time_home,
                        "over25_count_half_time_home": over25_count_half_time_home,
                        "over05_count_half_time_away": over05_count_half_time_away,
                        "over15_count_half_time_away": over15_count_half_time_away,
                        "over25_count_half_time_away": over25_count_half_time_away,
                        "corners_per_match": corners_per_match,
                        "corners_per_match_home": corners_per_match_home,
                        "corners_per_match_away": corners_per_match_away,
                        "cards_per_match": cards_per_match,
                        "cards_per_match_home": cards_per_match_home,
                        "cards_per_match_away": cards_per_match_away,
                        "xg_for_avg_overall": xg_for_avg_overall,
                        "xg_for_avg_home": xg_for_avg_home,
                        "xg_for_avg_away": xg_for_avg_away,
                        "xg_against_avg_overall": xg_against_avg_overall,
                        "xg_against_avg_home": xg_against_avg_home,
                        "xg_against_avg_away": xg_against_avg_away,
                        "matches_played":matches_played
                    }
        print(country)
        # GlobalTeam veritabanını güncelleyelim:
        for key, data in global_data.items():
            with transaction.atomic():
                GlobalTeam.objects.update_or_create(
                    team_name=key,
                    defaults=data
                )
