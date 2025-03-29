import numpy as np
import pandas as pd
import subprocess
import os

# sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Grafik için
import matplotlib.pyplot as plt

# Poisson (opsiyonel ek hesaplamalar için)
import scipy.stats

# Eğer XML -> CSV dönüşümünüz varsa (opsiyonel)

# ----------------------------------------------------------------
# 1) CSV Dosyalarını Yükle
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# 2) Eğer 'status' sütunu varsa, sadece "complete" statüsündeki maçları filtrele
# ----------------------------------------------------------------
def betprogram(df_teams, df_matches, fixture):
    if "status" in df_matches.columns:
        df_matches = df_matches[df_matches["status"].str.lower() == "complete"]
        print("\n=== Filtrelenmiş MATCH RESULTS (status='complete') ===")
        print(df_matches.head())
    else:
        print("\n[!] 'status' sütunu bulunamadı; tüm maçlar kullanılacak.")

    # ----------------------------------------------------------------
    # 3) teams_data Sözlüğü Oluşturma (Takım Bazlı Veriler)
    # ----------------------------------------------------------------
    teams_data = {}
    for index, row in df_teams.iterrows():
        t = row["common_name"]
    
        wins = row["wins"] if not pd.isna(row["wins"]) else 0
        wins_home = row["wins_home"] if not pd.isna(row["wins_home"]) else 0
        wins_away = row["wins_away"] if not pd.isna(row["wins_away"]) else 0
        draws = row["draws"] if not pd.isna(row["draws"]) else 0
        draws_home = row["draws_home"] if not pd.isna(row["draws_home"]) else 0
        draws_away = row["draws_away"] if not pd.isna(row["draws_away"]) else 0
        losses = row["losses"] if not pd.isna(row["losses"]) else 0
        losses_home = row["losses_home"] if not pd.isna(row["losses_home"]) else 0
        losses_away = row["losses_away"] if not pd.isna(row["losses_away"]) else 0
        goals_scored = row["goals_scored"] if not pd.isna(row["goals_scored"]) else 0
        goals_scored_home = row["goals_scored_home"] if not pd.isna(row["goals_scored_home"]) else 0
        goals_scored_away = row["goals_scored_away"] if not pd.isna(row["goals_scored_away"]) else 0
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
    
        teams_data[t] = {
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
            "xg_against_avg_away": xg_against_avg_away
        }

    # ----------------------------------------------------------------
    # 4) Feature Engineering: Historical Data Oluşturma
    # ----------------------------------------------------------------
    historical_data = []

    # "Complete" olduğuna emin olduğumuz temel sütunları kontrol edelim.
    required_cols = ["home_team_name", "away_team_name", "home_team_goal_count", "away_team_goal_count",
                     "home_team_goal_count_half_time", "away_team_goal_count_half_time",
                     "home_team_corner_count", 'away_team_corner_count', 
                     'home_team_yellow_cards', 'home_team_red_cards', 
                     'away_team_yellow_cards', 'away_team_red_cards', 
                     'home_team_first_half_cards', 'home_team_second_half_cards', 
                     'away_team_first_half_cards', 'away_team_second_half_cards', 
                     'home_team_shots', 'away_team_shots', 
                     'home_team_shots_on_target', 'away_team_shots_on_target',
                     'home_team_possession', 'away_team_possession',
                     'Away Team Pre-Match xG', 'team_a_xg', 'team_b_xg']

    for index, row in df_matches.iterrows():
        if row[required_cols].isnull().any():
            continue
        home = row["home_team_name"]
        away = row["away_team_name"]
        home_team_goal_count = row["home_team_goal_count"]
        away_team_goal_count = row["away_team_goal_count"]
        home_team_goal_count_half_time = row["home_team_goal_count_half_time"]
        away_team_goal_count_half_time = row["away_team_goal_count_half_time"]
        home_team_corner_count = row["home_team_corner_count"]
        away_team_corner_count = row["away_team_corner_count"]
        home_team_yellow_cards = row["home_team_yellow_cards"]
        home_team_red_cards = row["home_team_red_cards"]
        away_team_yellow_cards = row["away_team_yellow_cards"]
        away_team_red_cards = row["away_team_red_cards"]
        home_team_first_half_cards = row["home_team_first_half_cards"]
        home_team_second_half_cards = row["home_team_second_half_cards"]
        away_team_first_half_cards = row["away_team_first_half_cards"]
        away_team_second_half_cards = row["away_team_second_half_cards"]
        home_team_shots = row["home_team_shots"]
        away_team_shots = row["away_team_shots"]
        home_team_shots_on_target = row["home_team_shots_on_target"]
        away_team_shots_on_target = row["away_team_shots_on_target"]
        home_team_possession = row["home_team_possession"]
        away_team_possession = row["away_team_possession"]
        away_team_pre_match_xG = row["Away Team Pre-Match xG"]
        team_a_xg = row["team_a_xg"]
        team_b_xg = row["team_b_xg"]

        # Eğer teams_data'da bu takımlar yoksa atla.
        if home not in teams_data or away not in teams_data:
            continue

        # Takım istatistiklerini çekelim
        home_wins = teams_data[home]["wins"]
        away_wins = teams_data[away]["wins"]
        home_wins_home = teams_data[home]["wins_home"]
        away_wins_home = teams_data[away]["wins_home"]
        home_wins_away = teams_data[home]["wins_away"]
        away_wins_away = teams_data[away]["wins_away"]
        home_draws = teams_data[home]["draws"]
        away_draws = teams_data[away]["draws"]
        home_draws_home = teams_data[home]["draws_home"]
        away_draws_home = teams_data[away]["draws_home"]
        home_draws_away = teams_data[home]["draws_away"]
        away_draws_away = teams_data[away]["draws_away"]
        home_losses = teams_data[home]["losses"]
        away_losses = teams_data[away]["losses"]
        home_losses_home = teams_data[home]["losses_home"]
        away_losses_home = teams_data[away]["losses_home"]
        home_losses_away = teams_data[home]["losses_away"]
        away_losses_away = teams_data[away]["losses_away"]
        home_goals_scored = teams_data[home]["goals_scored"]
        away_goals_scored = teams_data[away]["goals_scored"]
        home_goals_scored_home = teams_data[home]["goals_scored_home"]
        away_goals_scored_home = teams_data[away]["goals_scored_home"]
        home_goals_scored_away = teams_data[home]["goals_scored_away"]
        away_goals_scored_away = teams_data[away]["goals_scored_away"]
        home_corners_total = teams_data[home]["corners_total"]
        away_corners_total = teams_data[away]["corners_total"]
        home_corners_total_home = teams_data[home]["corners_total_home"]
        away_corners_total_home = teams_data[away]["corners_total_home"]
        home_corners_total_away = teams_data[home]["corners_total_away"]
        away_corners_total_away = teams_data[away]["corners_total_away"]
        home_cards_total = teams_data[home]["cards_total"]
        away_cards_total = teams_data[away]["cards_total"]
        home_cards_total_home = teams_data[home]["cards_total_home"]
        away_cards_total_home = teams_data[away]["cards_total_home"]
        home_cards_total_away = teams_data[home]["cards_total_away"]
        away_cards_total_away = teams_data[away]["cards_total_away"]
        home_average_possession = teams_data[home]["average_possession"]
        away_average_possession = teams_data[away]["average_possession"]
        home_average_possession_home = teams_data[home]["average_possession_home"]
        away_average_possession_home = teams_data[away]["average_possession_home"]
        home_average_possession_away = teams_data[home]["average_possession_away"]
        away_average_possession_away = teams_data[away]["average_possession_away"]
        home_shots = teams_data[home]["shots"]
        away_shots = teams_data[away]["shots"]
        home_shots_home = teams_data[home]["shots_home"]
        away_shots_home = teams_data[away]["shots_home"]
        home_shots_away = teams_data[home]["shots_away"]
        away_shots_away = teams_data[away]["shots_away"]
        home_shots_on_target = teams_data[home]["shots_on_target"]
        away_shots_on_target = teams_data[away]["shots_on_target"]
        home_shots_on_target_home = teams_data[home]["shots_on_target_home"]
        away_shots_on_target_home = teams_data[away]["shots_on_target_home"]
        home_shots_on_target_away = teams_data[home]["shots_on_target_away"]
        away_shots_on_target_away = teams_data[away]["shots_on_target_away"]
        home_goals_scored_half_time = teams_data[home]["goals_scored_half_time"]
        away_goals_scored_half_time = teams_data[away]["goals_scored_half_time"]
        home_goals_scored_half_time_home = teams_data[home]["goals_scored_half_time_home"]
        away_goals_scored_half_time_home = teams_data[away]["goals_scored_half_time_home"]
        home_goals_scored_half_time_away = teams_data[home]["goals_scored_half_time_away"]
        away_goals_scored_half_time_away = teams_data[away]["goals_scored_half_time_away"]
        home_leading_at_half_time = teams_data[home]["leading_at_half_time"]
        away_leading_at_half_time = teams_data[away]["leading_at_half_time"]
        home_leading_at_half_time_home = teams_data[home]["leading_at_half_time_home"]
        away_leading_at_half_time_home = teams_data[away]["leading_at_half_time_home"]
        home_leading_at_half_time_away = teams_data[home]["leading_at_half_time_away"]
        away_leading_at_half_time_away = teams_data[away]["leading_at_half_time_away"]
        home_draw_at_half_time = teams_data[home]["draw_at_half_time"]
        away_draw_at_half_time = teams_data[away]["draw_at_half_time"]
        home_draw_at_half_time_home = teams_data[home]["draw_at_half_time_home"]
        away_draw_at_half_time_home = teams_data[away]["draw_at_half_time_home"]
        home_draw_at_half_time_away = teams_data[home]["draw_at_half_time_away"]
        away_draw_at_half_time_away = teams_data[away]["draw_at_half_time_away"]
        home_losing_at_half_time = teams_data[home]["losing_at_half_time"]
        away_losing_at_half_time = teams_data[away]["losing_at_half_time"]
        home_losing_at_half_time_home = teams_data[home]["losing_at_half_time_home"]
        away_losing_at_half_time_home = teams_data[away]["losing_at_half_time_home"]
        home_losing_at_half_time_away = teams_data[home]["losing_at_half_time_away"]
        away_losing_at_half_time_away = teams_data[away]["losing_at_half_time_away"]
        home_over05_count = teams_data[home]["over05_count"]
        away_over05_count = teams_data[away]["over05_count"]
        home_over15_count = teams_data[home]["over15_count"]
        away_over15_count = teams_data[away]["over15_count"]
        home_over25_count = teams_data[home]["over25_count"]
        away_over25_count = teams_data[away]["over25_count"]
        home_over35_count = teams_data[home]["over35_count"]
        away_over35_count = teams_data[away]["over35_count"]
        home_over05_count_home = teams_data[home]["over05_count_home"]
        away_over05_count_home = teams_data[away]["over05_count_home"]
        home_over15_count_home = teams_data[home]["over15_count_home"]
        away_over15_count_home = teams_data[away]["over15_count_home"]
        home_over25_count_home = teams_data[home]["over25_count_home"]
        away_over25_count_home = teams_data[away]["over25_count_home"]
        home_over35_count_home = teams_data[home]["over35_count_home"]
        away_over35_count_home = teams_data[away]["over35_count_home"]
        home_over45_count_home = teams_data[home]["over45_count_home"]
        away_over45_count_home = teams_data[away]["over45_count_home"]
        home_over55_count_home = teams_data[home]["over55_count_home"]
        away_over55_count_home = teams_data[away]["over55_count_home"]
        home_over05_count_away = teams_data[home]["over05_count_away"]
        away_over05_count_away = teams_data[away]["over05_count_away"]
        home_over15_count_away = teams_data[home]["over15_count_away"]
        away_over15_count_away = teams_data[away]["over15_count_away"]
        home_over25_count_away = teams_data[home]["over25_count_away"]
        away_over25_count_away = teams_data[away]["over25_count_away"]
        home_over35_count_away = teams_data[home]["over35_count_away"]
        away_over35_count_away = teams_data[away]["over35_count_away"]
        home_over05_count_half_time = teams_data[home]["over05_count_half_time"]
        away_over05_count_half_time = teams_data[away]["over05_count_half_time"]
        home_over15_count_half_time = teams_data[home]["over15_count_half_time"]
        away_over15_count_half_time = teams_data[away]["over15_count_half_time"]
        home_over25_count_half_time = teams_data[home]["over25_count_half_time"]
        away_over25_count_half_time = teams_data[away]["over25_count_half_time"]
        home_over05_count_half_time_home = teams_data[home]["over05_count_half_time_home"]
        away_over05_count_half_time_home = teams_data[away]["over05_count_half_time_home"]
        home_over15_count_half_time_home = teams_data[home]["over15_count_half_time_home"]
        away_over15_count_half_time_home = teams_data[away]["over15_count_half_time_home"]
        home_over25_count_half_time_home = teams_data[home]["over25_count_half_time_home"]
        away_over25_count_half_time_home = teams_data[away]["over25_count_half_time_home"]
        home_over05_count_half_time_away = teams_data[home]["over05_count_half_time_away"]
        away_over05_count_half_time_away = teams_data[away]["over05_count_half_time_away"]
        home_over15_count_half_time_away = teams_data[home]["over15_count_half_time_away"]
        away_over15_count_half_time_away = teams_data[away]["over15_count_half_time_away"]
        home_over25_count_half_time_away = teams_data[home]["over25_count_half_time_away"]
        away_over25_count_half_time_away = teams_data[away]["over25_count_half_time_away"]
        home_corners_per_match = teams_data[home]["corners_per_match"]
        away_corners_per_match = teams_data[away]["corners_per_match"]
        home_corners_per_match_home = teams_data[home]["corners_per_match_home"]
        away_corners_per_match_home = teams_data[away]["corners_per_match_home"]
        home_corners_per_match_away = teams_data[home]["corners_per_match_away"]
        away_corners_per_match_away = teams_data[away]["corners_per_match_away"]
        home_cards_per_match = teams_data[home]["cards_per_match"]
        away_cards_per_match = teams_data[away]["cards_per_match"]
        home_xg_for_avg_overall = teams_data[home]["xg_for_avg_overall"]
        away_xg_for_avg_overall = teams_data[away]["xg_for_avg_overall"]
        home_xg_for_avg_home = teams_data[home]["xg_for_avg_home"]
        away_xg_for_avg_home = teams_data[away]["xg_for_avg_home"]
        home_xg_for_avg_away = teams_data[home]["xg_for_avg_away"]
        away_xg_for_avg_away = teams_data[away]["xg_for_avg_away"]
        home_xg_against_avg_overall = teams_data[home]["xg_against_avg_overall"]
        away_xg_against_avg_overall = teams_data[away]["xg_against_avg_overall"]
        home_xg_against_avg_home = teams_data[home]["xg_against_avg_home"]
        away_xg_against_avg_home = teams_data[away]["xg_against_avg_home"]
        home_xg_against_avg_away = teams_data[home]["xg_against_avg_away"]
        away_xg_against_avg_away = teams_data[away]["xg_against_avg_away"]

        # Maç sonucu etiketi: H, D, A
        if home_team_goal_count > away_team_goal_count:
            result = "H"
        elif away_team_goal_count > home_team_goal_count:
            result = "A"
        else:
            result = "D"

        # Over 2.5 etiketi (3+ gol)
        over25 = 1 if (home_team_goal_count + away_team_goal_count) >= 3 else 0
        home_xG = teams_data[home].get("xg_for_avg_overall", 0)
        away_xG = teams_data[away].get("xg_for_avg_overall", 0)
        home_poss = teams_data[home].get("average_possession", 0)
        away_poss = teams_data[away].get("average_possession", 0)
        expected_goals_home = (home_xG + teams_data[away].get("xg_against_avg_overall", 0)) / 2
        expected_goals_away = (away_xG + teams_data[home].get("xg_against_avg_overall", 0)) / 2

        exp_corners = (((teams_data[home]["corners_total"] + teams_data[away]["corners_total"]) / 2) / 10) + np.random.normal(0, 0.1)
        # Doğrudan tahmin edilen corner sayısı (yuvarlanmış tamsayı)
        predicted_corners = int(round(exp_corners))
        
        # Kart tahmini:
        exp_cards = (((teams_data[home]["cards_total"] + teams_data[away]["cards_total"]) / 2) / 10) + np.random.normal(0, 0.1)
        predicted_cards = int(round(exp_cards))
        
        # Historical data listesine ekle
        historical_data.append([
            # Maç bilgileri (df_matches'den)
            home, away,
            home_team_goal_count, away_team_goal_count,
            home_team_goal_count_half_time, away_team_goal_count_half_time,
            home_team_corner_count, away_team_corner_count,
            home_team_yellow_cards, home_team_red_cards,
            away_team_yellow_cards, away_team_red_cards,
            home_team_first_half_cards, home_team_second_half_cards,
            away_team_first_half_cards, away_team_second_half_cards,
            home_team_shots, away_team_shots,
            home_team_shots_on_target, away_team_shots_on_target,
            home_team_possession, away_team_possession,
            away_team_pre_match_xG, team_a_xg, team_b_xg,
            # Takım bazlı istatistikler (teams_data'dan)
            home_wins, home_wins_home, home_wins_away,
            home_draws, home_draws_home, home_draws_away,
            home_losses, home_losses_home, home_losses_away,
            away_wins, away_wins_home, away_wins_away,
            away_draws, away_draws_home, away_draws_away,
            away_losses, away_losses_home, away_losses_away,
            # Ek hesaplamalar
            expected_goals_home, expected_goals_away,
            result,
            over25,
            exp_corners,
            exp_cards
        ])

    # Tüm eklenen verileri temsil edecek sütun isimleri (columns)
    columns = [
        "HomeTeam", "AwayTeam",
        "HomeGoals", "AwayGoals",
        "HomeGoals_HT", "AwayGoals_HT",
        "HomeCorners", "AwayCorners",
        "HomeYellow", "HomeRed",
        "AwayYellow", "AwayRed",
        "HomeFirstHalfCards", "HomeSecondHalfCards",
        "AwayFirstHalfCards", "AwaySecondHalfCards",
        "HomeShots", "AwayShots",
        "HomeShotsOnTarget", "AwayShotsOnTarget",
        "HomePossession", "AwayPossession",
        "AwayPreMatch_xG", "TeamA_xG", "TeamB_xG",
        "HomeWins", "HomeWins_Home", "HomeWins_Away",
        "HomeDraws", "HomeDraws_Home", "HomeDraws_Away",
        "HomeLosses", "HomeLosses_Home", "HomeLosses_Away",
        "AwayWins", "AwayWins_Home", "AwayWins_Away",
        "AwayDraws", "AwayDraws_Home", "AwayDraws_Away",
        "AwayLosses", "AwayLosses_Home", "AwayLosses_Away",
        "ExpectedGoals_Home", "ExpectedGoals_Away",
        "Result", "Over2_5",
        "OverCorners_8_5", "OverCards_2_5"
    ]

    # Historical verilerden DataFrame oluşturalım
    df_historical = pd.DataFrame(historical_data, columns=columns)

    print("\n=== df_train Oluşan Verisi (İlk 5 Satır) ===")
    print(df_historical.head())

    # ----------------------------------------------------------------
    # 5) Model İçin Verileri Hazırlama: Bütün Sütun Başlıklarını Kullanma
    # ----------------------------------------------------------------
    drop_columns = ["HomeTeam", "AwayTeam", "Result", "HomeGoals", "AwayGoals", "Over2_5"]

    le_home = LabelEncoder()
    le_away = LabelEncoder()
    df_historical["HomeTeam"] = le_home.fit_transform(df_historical["HomeTeam"])
    df_historical["AwayTeam"] = le_away.fit_transform(df_historical["AwayTeam"])

    feature_cols = df_historical.columns.difference(drop_columns)

    print("\nFeature Columns:")
    print(feature_cols.tolist())

    X = df_historical[feature_cols]
    y = df_historical["Result"]  # H, D, A target

    # ----------------------------------------------------------------
    # 6) Model Eğitimi: RandomForestClassifier
    # ----------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n=== MAÇ SONUCU (H/D/A) MODEL PERFORMANSI ===")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix (H, D, A):")
    print(confusion_matrix(y_test, y_pred, labels=["H", "D", "A"]))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # ----------------------------------------------------------------
    # Feature Importance: Tüm kullanılan sütun başlıklarının önemini görüntüleme
    # ----------------------------------------------------------------
    importances = model.feature_importances_
    feature_names = X.columns
    indices = np.argsort(importances)[::-1]

    print("\n=== Feature Importances ===")
    for i in range(len(feature_names)):
        print(f"{i+1}. {feature_names[indices[i]]}: {importances[indices[i]]:.4f}")

    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(len(feature_names)), importances[indices], align="center")
    plt.xticks(range(len(feature_names)), feature_names[indices], rotation=45, ha="right")
    plt.xlabel("Özellikler")
    plt.ylabel("Önem Skoru")
    plt.tight_layout()
    plt.show()

    # ----------------------------------------------------------------
    # 7) Over 2.5 (3+ Gol) İçin Ayrı Model (Opsiyonel)
    # ----------------------------------------------------------------
    X_over = df_historical[feature_cols]
    y_over = df_historical["Over2_5"]

    Xo_train, Xo_test, yo_train, yo_test = train_test_split(
        X_over, y_over, test_size=0.2, random_state=42, stratify=y_over
    )

    model_over = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    model_over.fit(Xo_train, yo_train)

    yo_pred = model_over.predict(Xo_test)
    print("\n=== OVER 2.5 (3+ GOL) MODEL PERFORMANSI ===")
    print("Accuracy (Over2.5):", accuracy_score(yo_test, yo_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(yo_test, yo_pred))
    print(classification_report(yo_test, yo_pred))

    # ----------------------------------------------------------------
    # 8) Poisson ile 3+ Gol Olasılığı Fonksiyonu (Opsiyonel)
    # ----------------------------------------------------------------
    def poisson_prob_3plus(lmbda):
        """Toplam golün 3+ olma olasılığı (0,1,2 hariç)."""
        return 1 - (scipy.stats.poisson.pmf(0, lmbda) +
                    scipy.stats.poisson.pmf(1, lmbda) +
                    scipy.stats.poisson.pmf(2, lmbda))

    # ----------------------------------------------------------------
    # 9) YENİ MAÇLAR ÜZERİNDE 1000 KEZ SİMÜLASYON
    # ----------------------------------------------------------------
    new_matches = fixturecalculate(fixture)

    NUM_SIMULATIONS = 1000

    # Simülasyon sonuçlarını saklamak için sözlükler
    simulation_results = {m: [] for m in new_matches}      # H/D/A tahmini listesi
    simulation_over25 = {m: [] for m in new_matches}         # Over2.5 tahmini (0/1)
    simulation_poisson = {m: [] for m in new_matches}        # Poisson ile 3+ gol olasılıkları
    simulation_corners = {m: [] for m in new_matches}
    simulation_cards = {m: [] for m in new_matches}
    simulation_scores = {m: {} for m in new_matches}
    # --- Yeni eklenen: İki Takımın Gol Atması (BTTS) sonuçları ---
    simulation_btts = {m: [] for m in new_matches}
    match_rows = []

    for match in new_matches:
        home, away,date = match
        if home not in teams_data or away not in teams_data:
            print(f"[!] Takım verisi eksik: {home} / {away}")
            continue

        for _ in range(NUM_SIMULATIONS):
            # Ev sahibi avantajına rastgele küçük sapma
            exp_g_home = ((teams_data[home]["xg_for_avg_overall"] + teams_data[away]["xg_against_avg_overall"]) / 2) + np.random.normal(0, 0.05)
            exp_g_away = ((teams_data[away]["xg_for_avg_overall"] + teams_data[home]["xg_against_avg_overall"]) / 2) + np.random.normal(0, 0.05)

            exp_g_home = max(exp_g_home, 0.01)
            exp_g_away = max(exp_g_away, 0.01)

            home_goals = np.random.poisson(exp_g_home)
            away_goals = np.random.poisson(exp_g_away)

            home_goals = home_goals if home_goals < 5 else 5
            away_goals = away_goals if away_goals < 5 else 5

            score = (home_goals, away_goals)
            simulation_scores[match][score] = simulation_scores[match].get(score, 0) + 1

            exp_corners = (((teams_data[home]["corners_total"] + teams_data[away]["corners_total"]) / 2) / 10) + np.random.normal(0, 0.1)
            predicted_corners = int(round(exp_corners))
            simulation_corners[match].append(predicted_corners)

            exp_cards = (((teams_data[home]["cards_total"] + teams_data[away]["cards_total"]) / 2) / 10) + np.random.normal(0, 0.1)
            predicted_cards = int(round(exp_cards))
            simulation_cards[match].append(predicted_cards)

            # --- Yeni eklenen: BTTS hesaplaması ---
            btts = 1 if home_goals > 0 and away_goals > 0 else 0
            simulation_btts[match].append(btts)

            row_dict = {
                "HomeTeam": home,
                "AwayTeam": away,
                "HomeGoals": 0,
                "AwayGoals": 0,
                "HomeGoals_HT": 0,
                "AwayGoals_HT": 0,
                "HomeCorners": teams_data[home]["corners_total"],
                "AwayCorners": teams_data[away]["corners_total"],
                "HomeYellow": teams_data[home]["cards_total"],
                "HomeRed": 0,
                "AwayYellow": teams_data[away]["cards_total"],
                "AwayRed": 0,
                "HomeFirstHalfCards": teams_data[home]["over05_count_half_time_home"],
                "HomeSecondHalfCards": teams_data[home]["over05_count_half_time_away"],
                "AwayFirstHalfCards": teams_data[away]["over05_count_half_time_home"],
                "AwaySecondHalfCards": teams_data[away]["over05_count_half_time_away"],
                "HomeShots": teams_data[home]["shots"],
                "AwayShots": teams_data[away]["shots"],
                "HomeShotsOnTarget": teams_data[home]["shots_on_target"],
                "AwayShotsOnTarget": teams_data[away]["shots_on_target"],
                "HomePossession": teams_data[home]["average_possession"],
                "AwayPossession": teams_data[away]["average_possession"],
                "AwayPreMatch_xG": row["Away Team Pre-Match xG"],
                "TeamA_xG": row["team_a_xg"],
                "TeamB_xG": row["team_b_xg"],
                "HomeWins": teams_data[home]["wins"],
                "HomeWins_Home": teams_data[home]["wins_home"],
                "HomeWins_Away": teams_data[home]["wins_away"],
                "HomeDraws": teams_data[home]["draws"],
                "HomeDraws_Home": teams_data[home]["draws_home"],
                "HomeDraws_Away": teams_data[home]["draws_away"],
                "HomeLosses": teams_data[home]["losses"],
                "HomeLosses_Home": teams_data[home]["losses_home"],
                "HomeLosses_Away": teams_data[home]["losses_away"],
                "AwayWins": teams_data[away]["wins"],
                "AwayWins_Home": teams_data[away]["wins_home"],
                "AwayWins_Away": teams_data[away]["wins_away"],
                "AwayDraws": teams_data[away]["draws"],
                "AwayDraws_Home": teams_data[away]["draws_home"],
                "AwayDraws_Away": teams_data[away]["draws_away"],
                "AwayLosses": teams_data[away]["losses"],
                "AwayLosses_Home": teams_data[away]["losses_home"],
                "AwayLosses_Away": teams_data[away]["losses_away"],
                "ExpectedGoals_Home": exp_g_home,
                "ExpectedGoals_Away": exp_g_away,
                "Result": result,
                "Over2_5": over25,
                "OverCorners_8_5": predicted_corners,
                "OverCards_2_5": predicted_cards,
            }

            df_new = pd.DataFrame([row_dict])
            drop_columns = ["HomeTeam", "AwayTeam", "Result", "HomeGoals", "AwayGoals", "Over2_5"]
            feature_cols = df_historical.columns.difference(drop_columns)
            df_new = df_new[feature_cols]
            proba_result = model.predict_proba(df_new)[0]
            classes_ = model.classes_
            result_pick = np.random.choice(classes_, p=proba_result)
            simulation_results[match].append(result_pick)

            proba_over2 = model_over.predict_proba(df_new)[0]
            pick_over = np.random.choice([0, 1], p=proba_over2)
            simulation_over25[match].append(pick_over)

            lam_total = exp_g_home + exp_g_away
            p_3plus = poisson_prob_3plus(lam_total)
            simulation_poisson[match].append(p_3plus)

    # ----------------------------------------------------------------
    # 10) 1000 Simülasyonun Özetini Ekrana Basma
    # ----------------------------------------------------------------
    sonuc = []
    print(f"\n=== {NUM_SIMULATIONS} Simülasyonun SONUÇLARI ===")
    for match in new_matches:
        home, away,date = match
        results = simulation_results[match]
        overs = simulation_over25[match]
        poisson_list = simulation_poisson[match]
        corners_list = simulation_corners[match]
        cards_list = simulation_cards[match]
        unique_corners, counts_corners = np.unique(corners_list, return_counts=True)
        freq_corners = dict(zip(unique_corners, counts_corners))
        sorted_corners = sorted(freq_corners.items(), key=lambda x: x[1], reverse=True)
        top5_corners = sorted_corners[:5]
        unique_cards, counts_cards = np.unique(cards_list, return_counts=True)
        freq_cards = dict(zip(unique_cards, counts_cards))
        sorted_cards = sorted(freq_cards.items(), key=lambda x: x[1], reverse=True)
        top5_cards = sorted_cards[:5]
        
        h_wins = results.count("H")
        d_wins = results.count("D")
        a_wins = results.count("A")
        over_count = sum(overs)
        over_ratio = (over_count / len(overs)) * 100 if len(overs) > 0 else 0
        avg_poisson_3plus = np.mean(poisson_list) if len(poisson_list) > 0 else 0

        # BTTS sonuçlarının hesaplanması
        btts_count = sum(simulation_btts[match])
        btts_ratio = (btts_count / NUM_SIMULATIONS) * 100 if len(simulation_btts[match]) > 0 else 0

        score_freq = simulation_scores[match]
        sorted_scores = sorted(score_freq.items(), key=lambda x: x[1], reverse=True)
        scores_with_pct = [(score, count, count/NUM_SIMULATIONS*100) for score, count in sorted_scores]
        first_half_scores = {}
        second_half_scores = {}
        match_results_from_half = {}
        ht_h2_count = 0
        at_h2_count = 0
        for _ in range(NUM_SIMULATIONS):
            ht_home_goals = np.random.poisson(exp_g_home / 2)
            ht_away_goals = np.random.poisson(exp_g_away / 2)
            ft_home_goals = np.random.poisson(exp_g_home)
            ft_away_goals = np.random.poisson(exp_g_away)

            ht_score = (ht_home_goals, ht_away_goals)
            ft_score = (ft_home_goals, ft_away_goals)

            first_half_scores[ht_score] = first_half_scores.get(ht_score, 0) + 1
            second_half_home_goals = max(0, ft_home_goals - ht_home_goals)
            second_half_away_goals = max(0, ft_away_goals - ht_away_goals)
            second_half_score = (second_half_home_goals, second_half_away_goals)
            second_half_scores[second_half_score] = second_half_scores.get(second_half_score, 0) + 1
            match_results_from_half[(ht_score, second_half_score)] = match_results_from_half.get((ht_score, second_half_score), 0) + 1

            if ht_home_goals > ht_away_goals:
                ht_winner = "H"
            elif ht_away_goals > ht_home_goals:
                ht_winner = "A"
            else:
                ht_winner = "D"

            if ft_home_goals > ft_away_goals:
                ft_winner = "H"
            elif ft_away_goals > ft_home_goals:
                ft_winner = "A"
            else:
                ft_winner = "D"

            if ht_winner == "H" and ft_winner == "A":
                ht_h2_count += 1
            if ht_winner == "A" and ft_winner == "H":
                at_h2_count += 1

            first_half_score = (ht_home_goals, ht_away_goals)
            first_half_scores[first_half_score] = first_half_scores.get(first_half_score, 0) + 1    

        sorted_half_scores = sorted(first_half_scores.items(), key=lambda x: x[1], reverse=True)
        half_scores_with_pct = [(score, count, count/NUM_SIMULATIONS*100) for score, count in sorted_half_scores]

        sorted_second_half_scores = sorted(second_half_scores.items(), key=lambda x: x[1], reverse=True)
        second_half_scores_with_pct = [(score, count, count/NUM_SIMULATIONS*100) for score, count in sorted_second_half_scores]

        sorted_match_results = sorted(match_results_from_half.items(), key=lambda x: x[1], reverse=True)
        match_results_with_pct = [(scores, count, count/NUM_SIMULATIONS*100) for scores, count in sorted_match_results]
        
        ht_h2_pct = (ht_h2_count / NUM_SIMULATIONS) * 100
        at_h2_pct = (at_h2_count / NUM_SIMULATIONS) * 100        

        top5_first_half = ", ".join([f"{score} ({pct:.2f}%)" for score, count, pct in half_scores_with_pct[:5]])
        top5_final = ", ".join([f"{score} ({pct:.2f}%)" for score, count, pct in scores_with_pct[:5]])
        top3_combo = ", ".join([f"İlk Yarı: {scores[0]}, İkinci Yarı: {scores[1]} -> Final: ({scores[0][0]+scores[1][0]}, {scores[0][1]+scores[1][1]}) ({pct:.2f}%)"
                                    for scores, count, pct in match_results_with_pct[:3]])
        row_dict = {
            "HomeTeam":home,
            "AwayTeam":away,
            "MS1": round(h_wins/NUM_SIMULATIONS*100, 2),
            "MSX": round(d_wins/NUM_SIMULATIONS*100, 2),
            "MS2": round(a_wins/NUM_SIMULATIONS*100, 2),
            "KG VAR": round(btts_ratio, 2),
            "OVER2.5": round(over_ratio, 2),
            "DATE":date,
            
            
            # Buraya istediğiniz kadar ekstra sütun ekleyebilirsiniz:
            # "Top5_FirstHalfScore": top5_first_half_scores_str,
            # "Top3_Combo": top3_combo,
            # vs.
        }

        # Oluşturduğumuz bu satırı, "match_rows" listemize ekliyoruz
        match_rows.append(row_dict)
        print(f"\nMaç: {home} vs {away}")
        print(f"  🏠 Ev Sahibi Kazanma: {h_wins} / {NUM_SIMULATIONS} = %{h_wins/NUM_SIMULATIONS*100:.2f}")
        print(f"  🤝 Beraberlik: {d_wins} / {NUM_SIMULATIONS} = %{d_wins/NUM_SIMULATIONS*100:.2f}")
        print(f"  🚀 Deplasman Kazanma: {a_wins} / {NUM_SIMULATIONS} = %{a_wins/NUM_SIMULATIONS*100:.2f}")
        print(f"  🔥 İki Takımın Gol Atma (BTTS) Oranı: %{btts_ratio:.2f}")
        print(f"  🌐 Over 2.5 Oranı: %{over_ratio:.2f}")
        print(f"  🔥 Poisson 3+ Gol (ortalama): %{avg_poisson_3plus*100:.2f}")
        print(f"  ⚽ Tam Zamanlı Skor Dağılımı (Yüzdelikli):")
        for score, count, pct in scores_with_pct:
            print(f"      {score}: {count} kez (%{pct:.2f})")
        print(f"  🏆 İlk Yarı Skor Dağılımı (Yüzdelikli):")
        for score, count, pct in half_scores_with_pct:
            print(f"      {score}: {count} kez (%{pct:.2f})")

        print(f"  🔄 İlk Yarı Ev - Maç Sonu Deplasman (HT-H2): {ht_h2_count} kez (%{ht_h2_pct:.2f})")
        print(f"  🔄 İlk Yarı Deplasman - Maç Sonu Ev (AT-H2): {at_h2_count} kez (%{at_h2_pct:.2f})")    

        print(f"\n  ⚽ İlk Yarı & İkinci Yarı Kombinasyonları:")
        for (ht_score, sh_score), count, pct in match_results_with_pct:
            final_score = (ht_score[0] + sh_score[0], ht_score[1] + sh_score[1])
            print(f"      İlk Yarı: {ht_score},  İkinci Yarı: {sh_score}  ➝  Maç Sonu: {final_score}  (%{pct:.2f})")
        print(f"beklenen corner : {predicted_corners} beklenen card:{predicted_cards}")
        result_str = (f"Maç: {home} vs {away}: MS1: {h_wins/NUM_SIMULATIONS*100:.2f}%  "
                      f"MSX: {d_wins/NUM_SIMULATIONS*100:.2f}%  "
                      f"MS2: {a_wins/NUM_SIMULATIONS*100:.2f}%  "
                      f"BTTS: {btts_ratio:.2f}%  "
                      f"2.5 Üst: {over_ratio:.2f}%  "
                      f"Poisson: {avg_poisson_3plus*100:.2f}%\n"
                      f"KG VAR : {btts_ratio:.2f}%\n"
                      f"Top 5 İlk Yarı Skorları: {top5_first_half}\n"
                      f"Top 5 Maç Sonu Skorları: {top5_final}\n"
                      f"Top 3 Kombinasyon: {top3_combo}"
                      )
        
        sonuc.append(result_str)

    return match_rows

def fixturecalculate(df_matches):
    import pandas as pd
    first_incomplete_row = df_matches[df_matches["status"] == "incomplete"].iloc[0]
    gameweek_number = first_incomplete_row["Game Week"]
    filtered_matches = df_matches[df_matches["Game Week"] == gameweek_number]
    new_matches = [(row["home_team_name"], row["away_team_name"],row["date_GMT"]) for _, row in filtered_matches.iterrows()]
    return new_matches

# ----------------------------------------------------------------
# leagueselector() Fonksiyonu: stats klasöründeki ligleri ayıklar ve betprogram()'a gönderir.
# ----------------------------------------------------------------
def leagueselector():
    DATA_FOLDER = "stats"
    files = os.listdir(DATA_FOLDER)
    teams_files = [f for f in files if "teams" in f.lower() and f.endswith(".csv")]
    matches_files = [f for f in files if "matches" in f.lower() and f.endswith(".csv")]

    if not teams_files or not matches_files:
        print("[!] Uygun takım veya maç dosyaları bulunamadı.")
        return {}

    leagues = {}
    for file in teams_files:
        league = file.split("teams")[0].rstrip("-").strip()
        leagues.setdefault(league, {})["teams"] = os.path.join(DATA_FOLDER, file)
        
    for file in matches_files:
        league = file.split("matches")[0].rstrip("-").strip()
        leagues.setdefault(league, {})["matches"] = os.path.join(DATA_FOLDER, file)

    return leagues

leagues = leagueselector()
all_results = {}

leagues = leagueselector()

def result_printer(leagues):
    for league, paths in leagues.items():
        if "teams" in paths and "matches" in paths:
            print(f"\n>>> {league} için veriler okunuyor...")
            df_teams = pd.read_csv(paths["teams"], encoding="utf-8-sig")
            df_matches = pd.read_csv(paths["matches"], encoding="utf-8-sig")
            fixture = df_matches.copy()
            league_result = betprogram(df_teams, df_matches, fixture)
            all_results[league] = league_result

    for league, result_list in all_results.items():
        print(f"\n<<< {league} Sonuçları >>>")
        for res in result_list:
            print(res)
    return result_list        
     

all_results=result_printer(leagues)
for league, result_list in all_results.items():
    # "result_list" -> list of dict
    if not result_list:
        continue

    df_result = pd.DataFrame(result_list)
    csv_filename = f"{league.replace(' ','_')}_results.csv"
    
    # Her sütun (dict key’i) ayrı başlık olarak CSV’ye yazılır.
    df_result.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"{csv_filename} oluşturuldu.")

