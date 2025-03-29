# solo.py

import numpy as np
import pandas as pd
import subprocess
import os
import hashlib
import re
from pathlib import Path
import scipy.stats
import matplotlib.pyplot as plt
from datetime import datetime,timedelta


# sklearn modülleri
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Django modelimizi import edin (uygulama adınızı uygun şekilde düzenleyin)
from matches.models import MatchResult


# ----------------------------------------------------------------
# Yardımcı Fonksiyonlar
# ----------------------------------------------------------------
MONTHS_TR = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan",
    "05": "Mayıs", "06": "Haziran", "07": "Temmuz", "08": "Ağustos",
    "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"
}

def to_turkish_date_manual(iso_date_str):
    # "2025-02-22" => yıl=2025, ay=02, gün=22
    try:
        year, month, day = iso_date_str.split("-")
        ay_ismi = MONTHS_TR.get(month, month)
        return f"{int(day)} {ay_ismi}"
    except:
        return iso_date_str  # parse edemediysek orijinalini dön.
def parse_date_only(date_str):
    """
    "Feb 14 2025 - 8:00pm" gibi bir metni
    YYYY-MM-DD (örnek: "2025-02-14") formatına dönüştürür.
    """

    # Bazı CSV'lerde 'pm' küçük harfle geçebilir, strptime() varsayılan olarak "PM" bekler
    # Bu yüzden 'am'/'pm' -> 'AM'/'PM' çeviriyoruz:
    fixed_str = date_str.replace("am", "AM").replace("pm", "PM")

    # "%b %d %Y - %I:%M%p" => 
    #  %b   -> Ayın kısaltılmış ismi (Jan, Feb, Mar ...)
    #  %d   -> Gün (01-31)
    #  %Y   -> Yıl (4 haneli)
    #  -    -> Literal ' - '
    #  %I   -> Saat (12 saatlik format)
    #  :%M  -> Dakika
    #  %p   -> AM / PM
    dt = datetime.strptime(fixed_str, "%b %d %Y - %I:%M%p")

    # Sadece YYYY-MM-DD biçiminde döndür
    return dt.strftime("%Y-%m-%d")
def get_time(date_str):
    """
    "Feb 14 2025 - 8:00pm" gibi bir metni
    YYYY-MM-DD (örnek: "2025-02-14") formatına dönüştürür.
    """

    # Bazı CSV'lerde 'pm' küçük harfle geçebilir, strptime() varsayılan olarak "PM" bekler
    # Bu yüzden 'am'/'pm' -> 'AM'/'PM' çeviriyoruz:
    fixed_str = date_str.replace("am", "AM").replace("pm", "PM")
    dt = datetime.strptime(fixed_str, "%b %d %Y - %I:%M%p")
    # "%b %d %Y - %I:%M%p" => 
    #  %b   -> Ayın kısaltılmış ismi (Jan, Feb, Mar ...)
    #  %d   -> Gün (01-31)
    #  %Y   -> Yıl (4 haneli)
    #  -    -> Literal ' - '
    #  %I   -> Saat (12 saatlik format)
    #  :%M  -> Dakika
    #  %p   -> AM / PM
    dt_turkey=dt+timedelta(hours=3)
    
    
    # Sadece YYYY-MM-DD biçiminde döndür
    return dt_turkey.strftime("%H:%M")
def generate_stable_id(home, away):
    """
    Ev sahibi takım, deplasman takımı kullanılarak sabit 8 karakterlik id üretir.
    """
    unique_str = home + away
    return hashlib.md5(unique_str.encode('utf-8')).hexdigest()[:8]

def slugify_team_name(name):
    """
    Basit bir slugify örneği: Küçük harfe çevir, özel karakterleri tireye dönüştür.
    """
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

# ----------------------------------------------------------------
# betprogram Fonksiyonu
# ----------------------------------------------------------------
def betprogram(df_teams, df_matches, fixture, league_name=""):
    # 2) 'status' sütunu varsa sadece "complete" olanları filtrele
    if "status" in df_matches.columns:
        df_matches = df_matches[df_matches["status"].str.lower() == "complete"]
        print("\n=== Filtrelenmiş MATCH RESULTS (status='complete') ===")
        print(df_matches.head())
    else:
        print("\n[!] 'status' sütunu bulunamadı; tüm maçlar kullanılacak.")

    # 3) Takım bazlı veriler için sözlük oluşturma
    teams_data = {}
    for index, row in df_teams.iterrows():
        t = row["common_name"]
        teams_data[t] = {
            "wins": row["wins"] if not pd.isna(row["wins"]) else 0,
            "wins_home": row["wins_home"] if not pd.isna(row["wins_home"]) else 0,
            "wins_away": row["wins_away"] if not pd.isna(row["wins_away"]) else 0,
            "draws": row["draws"] if not pd.isna(row["draws"]) else 0,
            "draws_home": row["draws_home"] if not pd.isna(row["draws_home"]) else 0,
            "draws_away": row["draws_away"] if not pd.isna(row["draws_away"]) else 0,
            "losses": row["losses"] if not pd.isna(row["losses"]) else 0,
            "losses_home": row["losses_home"] if not pd.isna(row["losses_home"]) else 0,
            "losses_away": row["losses_away"] if not pd.isna(row["losses_away"]) else 0,
            "goals_scored": row["goals_scored"] if not pd.isna(row["goals_scored"]) else 0,
            "goals_scored_home": row["goals_scored_home"] if not pd.isna(row["goals_scored_home"]) else 0,
            "goals_scored_away": row["goals_scored_away"] if not pd.isna(row["goals_scored_away"]) else 0,
            "corners_total": row["corners_total"] if not pd.isna(row["corners_total"]) else 0,
            "corners_total_home": row["corners_total_home"] if not pd.isna(row["corners_total_home"]) else 0,
            "corners_total_away": row["corners_total_away"] if not pd.isna(row["corners_total_away"]) else 0,
            "cards_total": row["cards_total"] if not pd.isna(row["cards_total"]) else 0,
            "cards_total_home": row["cards_total_home"] if not pd.isna(row["cards_total_home"]) else 0,
            "cards_total_away": row["cards_total_away"] if not pd.isna(row["cards_total_away"]) else 0,
            "average_possession": row["average_possession"] if not pd.isna(row["average_possession"]) else 0,
            "average_possession_home": row["average_possession_home"] if not pd.isna(row["average_possession_home"]) else 0,
            "average_possession_away": row["average_possession_away"] if not pd.isna(row["average_possession_away"]) else 0,
            "shots": row["shots"] if not pd.isna(row["shots"]) else 0,
            "shots_home": row["shots_home"] if not pd.isna(row["shots_home"]) else 0,
            "shots_away": row["shots_away"] if not pd.isna(row["shots_away"]) else 0,
            "shots_on_target": row["shots_on_target"] if not pd.isna(row["shots_on_target"]) else 0,
            "shots_on_target_home": row["shots_on_target_home"] if not pd.isna(row["shots_on_target_home"]) else 0,
            "shots_on_target_away": row["shots_on_target_away"] if not pd.isna(row["shots_on_target_away"]) else 0,
            "xg_for_avg_overall": row["xg_for_avg_overall"] if not pd.isna(row["xg_for_avg_overall"]) else 0,
            "xg_against_avg_overall": row["xg_against_avg_overall"] if not pd.isna(row["xg_against_avg_overall"]) else 0,
            # Diğer istatistikler de eklenebilir...
        }

    # 4) Feature engineering ve historical data oluşturma
    historical_data = []
    required_cols = [
        "home_team_name", "away_team_name", "home_team_goal_count", "away_team_goal_count",
        "home_team_goal_count_half_time", "away_team_goal_count_half_time",
        "home_team_corner_count", "away_team_corner_count", 
        "home_team_yellow_cards", "home_team_red_cards", 
        "away_team_yellow_cards", "away_team_red_cards", 
        "home_team_first_half_cards", "home_team_second_half_cards", 
        "away_team_first_half_cards", "away_team_second_half_cards", 
        "home_team_shots", "away_team_shots", 
        "home_team_shots_on_target", "away_team_shots_on_target",
        "home_team_possession", "away_team_possession",
        "Away Team Pre-Match xG", "team_a_xg", "team_b_xg"
    ]
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

        # Takım istatistiklerini alalım
        home_xG = teams_data[home].get("xg_for_avg_overall", 0)
        away_xG = teams_data[away].get("xg_for_avg_overall", 0)
        expected_goals_home = (home_xG + teams_data[away].get("xg_against_avg_overall", 0)) / 2
        expected_goals_away = (away_xG + teams_data[home].get("xg_against_avg_overall", 0)) / 2

        # Maç sonucu etiketi: H, D, A
        if home_team_goal_count > away_team_goal_count:
            result = "H"
        elif away_team_goal_count > home_team_goal_count:
            result = "A"
        else:
            result = "D"

        # Over 2.5 (3+ gol) etiketi
        over25 = 1 if (home_team_goal_count + away_team_goal_count) >= 3 else 0
        
        # Ek hesaplamalar: Corner ve kart tahmini
        exp_corners = (((teams_data[home]["corners_total"] + teams_data[away]["corners_total"]) / 2) / 10) + np.random.normal(0, 0.1)
        predicted_corners = int(round(exp_corners))
        exp_cards = (((teams_data[home]["cards_total"] + teams_data[away]["cards_total"]) / 2) / 10) + np.random.normal(0, 0.1)
        predicted_cards = int(round(exp_cards))
        
        historical_data.append([
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
            expected_goals_home, expected_goals_away,
            result, over25, exp_corners, exp_cards
        ])
        
    # Sütun isimleri
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
        "ExpectedGoals_Home", "ExpectedGoals_Away",
        "Result", "Over2_5",
        "OverCorners_8_5", "OverCards_2_5",
    ]
    
    df_historical = pd.DataFrame(historical_data, columns=columns)
    print("\n=== df_train Oluşan Verisi (İlk 5 Satır) ===")
    print(df_historical.head())

    # Model için veri hazırlığı
    drop_columns = ["HomeTeam", "AwayTeam", "Result", "HomeGoals", "AwayGoals", "Over2_5"]
    le_home = LabelEncoder()
    le_away = LabelEncoder()
    df_historical["HomeTeam"] = le_home.fit_transform(df_historical["HomeTeam"])
    df_historical["AwayTeam"] = le_away.fit_transform(df_historical["AwayTeam"])
    feature_cols = df_historical.columns.difference(drop_columns)

    X = df_historical[feature_cols]
    y = df_historical["Result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)

    # Ayrı over2.5 modeli
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

    def poisson_prob_3plus(lmbda):
        """Toplam golün 3+ olma olasılığı (0,1,2 hariç)."""
        return 1 - (scipy.stats.poisson.pmf(0, lmbda) +
                    scipy.stats.poisson.pmf(1, lmbda) +
                    scipy.stats.poisson.pmf(2, lmbda))

    # 9) Yeni maçlar üzerinde simülasyon
    new_matches = fixturecalculate(fixture)
    NUM_SIMULATIONS = 1000

    simulation_results = {m: [] for m in new_matches}
    simulation_over25 = {m: [] for m in new_matches}
    simulation_poisson = {m: [] for m in new_matches}
    simulation_corners = {m: [] for m in new_matches}
    simulation_cards = {m: [] for m in new_matches}
    simulation_scores = {m: {} for m in new_matches}
    simulation_btts = {m: [] for m in new_matches}

    for match in new_matches:
        home, away, date = match
        if home not in teams_data or away not in teams_data:
            print(f"[!] Takım verisi eksik: {home} / {away}")
            continue
        for _ in range(NUM_SIMULATIONS):
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
            btts = 1 if home_goals > 0 and away_goals > 0 else 0
            simulation_btts[match].append(btts)

            row_dict = {
                "id": generate_stable_id(home, away),
                "league": league_name,
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
                "p_3plus":p_3plus,
            }

            # Özellik sütunlarını oluşturup model tahminlerini alıyoruz
            drop_columns = ["HomeTeam", "AwayTeam", "Result", "HomeGoals", "AwayGoals", "Over2_5"]
            feature_cols = df_historical.columns.difference(drop_columns)
            df_new = pd.DataFrame([row_dict])[feature_cols]
            proba_result = model.predict_proba(df_new)[0]
            result_pick = np.random.choice(model.classes_, p=proba_result)
            simulation_results[match].append(result_pick)
            proba_over2 = model_over.predict_proba(df_new)[0]
            pick_over = np.random.choice([0, 1], p=proba_over2)
            simulation_over25[match].append(pick_over)
            lam_total = exp_g_home + exp_g_away
            p_3plus = poisson_prob_3plus(lam_total)
            simulation_poisson[match].append(p_3plus)

    # 10) Simülasyon özetlerinin hazırlanması ve DB'ye kaydedilmesi
    match_rows = []
    for match in new_matches:
        home, away, date = match
        # Özet hesaplamalarını yapıp row_dict'i oluşturduktan sonra:
        home_slug = slugify_team_name(home)
        away_slug = slugify_team_name(away)
        row_dict = {
            "id": generate_stable_id(home, away),
            "league": league_name,
            "HomeTeam": home,
            "AwayTeam": away,
            "MS1": round(simulation_results[match].count("H") / NUM_SIMULATIONS * 100, 2),
            "MSX": round(simulation_results[match].count("D") / NUM_SIMULATIONS * 100, 2),
            "MS2": round(simulation_results[match].count("A") / NUM_SIMULATIONS * 100, 2),
            "KG": round((sum(simulation_btts[match]) / NUM_SIMULATIONS) * 100, 2),
            "over2_5": round((sum(simulation_over25[match]) / NUM_SIMULATIONS) * 100, 2),
            "p_3plus":round((sum(simulation_poisson[match]) / NUM_SIMULATIONS) * 100, 2),
            "DATE": parse_date_only(date.strip()),
            "TIME": get_time(date.strip()),
            "scores_with_pct": simulation_scores[match],
            "half_scores_with_pct": {},  # Eğer bu veriyi hesaplıyorsanız ekleyin
            "match_result_with_pct": {},   # Eğer hesaplanıyorsa ekleyin
            "top_5_first_half": "",        # Özet string'ler
            "top_5_final": "",
            "top3_combo": "",
            "home_team_logo": f"{home_slug}.png",
            "away_team_logo": f"{away_slug}.png",
        }
        # Veritabanına kaydet (update_or_create kullanarak)
        MatchResult.objects.update_or_create(
            id=row_dict["id"],
            defaults=row_dict
        )
        match_rows.append(row_dict)
        print(f"\nMaç: {home} vs {away} - ID: {row_dict['id']}")
    return match_rows

# ----------------------------------------------------------------
# Fixture ve Lig Seçici Fonksiyonlar
# ----------------------------------------------------------------
def fixturecalculate(df_matches):
    import pandas as pd
    first_incomplete_row = df_matches[df_matches["status"] == "incomplete"].iloc[0]
    gameweek_number = first_incomplete_row["Game Week"]
    filtered_matches = df_matches[df_matches["Game Week"] == gameweek_number]
    new_matches = [(row["home_team_name"], row["away_team_name"], row["date_GMT"]) for _, row in filtered_matches.iterrows()]
    return new_matches

def leagueselector():
    BASE_DIR = Path(__file__).resolve().parent  # betmodel dizini
    DATA_FOLDER = BASE_DIR / "stats"
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

def get_betprogram_results():
    leagues = leagueselector()
    all_results = {}
    for league, paths in leagues.items():
        if "teams" in paths and "matches" in paths:
            print(f"\n>>> {league} için veriler okunuyor...")
            df_teams = pd.read_csv(paths["teams"], encoding="utf-8-sig")
            df_matches = pd.read_csv(paths["matches"], encoding="utf-8-sig")
            fixture = df_matches.copy()
            league_result = betprogram(df_teams, df_matches, fixture, league_name=league)
            all_results[league] = league_result
    return all_results

if __name__ == '__main__':
    results = get_betprogram_results()
    print("Sonuçlar:")
    print(results)
