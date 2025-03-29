import os
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

def leagueselector(data_folder="deneme"):
    """
    data_folder içinde 'teams' ve 'matches' geçen CSV dosyalarını eşleştirir.
    Örneğin:
       - spain-teams-2024.csv
       - spain-matches-2024.csv
    gibi dosyaları algılar ve leagues[spain]["teams"] / leagues[spain]["matches"] şeklinde döndürür.
    """
    files = os.listdir(data_folder)
    teams_files = [f for f in files if "teams" in f.lower() and f.endswith(".csv")]
    matches_files = [f for f in files if "matches" in f.lower() and f.endswith(".csv")]

    leagues = {}
    for file in teams_files:
        league = file.split("teams")[0].rstrip("-").strip()
        leagues.setdefault(league, {})["teams"] = os.path.join(data_folder, file)
    
    for file in matches_files:
        league = file.split("matches")[0].rstrip("-").strip()
        leagues.setdefault(league, {})["matches"] = os.path.join(data_folder, file)

    return leagues

def train_corners_cards(df_matches):
    """
    'complete' durumdaki maçlardan OverCorners_8_5 ve OverCards_2_5 modellerini eğitir,
    encode bilgilerini döndürür.
    """

    # Sadece complete maçlar
    df_complete = df_matches[df_matches["status"].str.lower() == "complete"].copy()
    if df_complete.empty:
        print("Complete maç yok. Model eğitilemeyecek.")
        return None, None, None, None, None, None

    # Gerekli sütunlar yoksa hata vermeden atla
    required_cols = [
        "home_team_name", "away_team_name",
        "home_team_corner_count", "away_team_corner_count",
        "home_team_yellow_cards", "home_team_red_cards",
        "away_team_yellow_cards", "away_team_red_cards"
    ]
    for col in required_cols:
        if col not in df_complete.columns:
            print(f"Kolon eksik: {col}")
            return None, None, None, None, None, None

    # Eksik satırları at
    df_complete.dropna(subset=required_cols, inplace=True)
    if df_complete.empty:
        print("Complete maç verisinde gereken kolonlar eksik veya NaN.")
        return None, None, None, None, None, None

    # Köşe + Kart hesapla
    df_complete["TotalCorners"] = df_complete["home_team_corner_count"] + df_complete["away_team_corner_count"]
    df_complete["HomeCards"] = df_complete["home_team_yellow_cards"] + df_complete["home_team_red_cards"]
    df_complete["AwayCards"] = df_complete["away_team_yellow_cards"] + df_complete["away_team_red_cards"]
    df_complete["TotalCards"] = df_complete["HomeCards"] + df_complete["AwayCards"]

    # Over 8.5 corners ve over 2.5 cards
    df_complete["OverCorners_8_5"] = (df_complete["TotalCorners"] > 8.5).astype(int)
    df_complete["OverCards_2_5"] = (df_complete["TotalCards"] > 2.5).astype(int)

    # Takım isimlerini encode et
    le_home = LabelEncoder()
    le_away = LabelEncoder()
    df_complete["HomeTeam_encoded"] = le_home.fit_transform(df_complete["home_team_name"])
    df_complete["AwayTeam_encoded"] = le_away.fit_transform(df_complete["away_team_name"])

    # Feature set: sade
    features = ["HomeTeam_encoded", "AwayTeam_encoded"]
    X = df_complete[features].copy()

    # MODELLER
    # 1) OverCorners_8_5
    y_corners = df_complete["OverCorners_8_5"].copy()
    # 2) OverCards_2_5
    y_cards = df_complete["OverCards_2_5"].copy()

    # MODELLERİ EĞİT
    model_corners = None
    model_cards = None

    # Köşe Modeli
    if len(y_corners.unique()) < 2:
        print("Köşe (OverCorners_8_5) için tek sınıf var; model eğitilemez.")
    else:
        try:
            Xc_train, Xc_test, yc_train, yc_test = train_test_split(X, y_corners, 
                                                                    test_size=0.2, 
                                                                    random_state=42, 
                                                                    stratify=y_corners)
        except ValueError as e:
            print(f"Stratify hatası (köşe): {e} -> stratify=None ile devam ediliyor.")
            Xc_train, Xc_test, yc_train, yc_test = train_test_split(X, y_corners, 
                                                                    test_size=0.2, 
                                                                    random_state=42,
                                                                    stratify=None)

        model_corners = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
        model_corners.fit(Xc_train, yc_train)

        pred_corners = model_corners.predict(Xc_test)
        print("\n=== Köşe Modeli (Over8.5) Eğitim Sonucu ===")
        print("Accuracy:", accuracy_score(yc_test, pred_corners))
        print("Confusion Matrix:\n", confusion_matrix(yc_test, pred_corners))
        print(classification_report(yc_test, pred_corners))

    # Kart Modeli
    if len(y_cards.unique()) < 2:
        print("Kart (OverCards_2_5) için tek sınıf var; model eğitilemez.")
    else:
        try:
            Xca_train, Xca_test, yca_train, yca_test = train_test_split(X, y_cards,
                                                                        test_size=0.2,
                                                                        random_state=42,
                                                                        stratify=y_cards)
        except ValueError as e:
            print(f"Stratify hatası (kart): {e} -> stratify=None ile devam ediliyor.")
            Xca_train, Xca_test, yca_train, yca_test = train_test_split(X, y_cards,
                                                                        test_size=0.2,
                                                                        random_state=42,
                                                                        stratify=None)
        model_cards = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
        model_cards.fit(Xca_train, yca_train)

        pred_cards = model_cards.predict(Xca_test)
        print("\n=== Kart Modeli (Over2.5) Eğitim Sonucu ===")
        print("Accuracy:", accuracy_score(yca_test, pred_cards))
        print("Confusion Matrix:\n", confusion_matrix(yca_test, pred_cards))
        print(classification_report(yca_test, pred_cards))

    return model_corners, model_cards, le_home, le_away, features, df_complete

def predict_incomplete_corners_cards(df_matches, model_corners, model_cards, le_home, le_away, features):
    """
    'incomplete' durumundaki maçlar için OverCorners_8_5 ve OverCards_2_5 tahmini yapar.
    """
    df_incomplete = df_matches[df_matches["status"].str.lower() == "incomplete"].copy()
    if df_incomplete.empty:
        print("Incomplete maç yok.")
        return

    # Aynı alanların varlığını kontrol edelim
    required_cols = ["home_team_name", "away_team_name"]
    for col in required_cols:
        if col not in df_incomplete.columns:
            print(f"Incomplete maçlarda eksik kolon: {col}")
            return

    # HomeTeam_encoded, AwayTeam_encoded
    df_incomplete["HomeTeam_encoded"] = le_home.transform(df_incomplete["home_team_name"])
    df_incomplete["AwayTeam_encoded"] = le_away.transform(df_incomplete["away_team_name"])

    # Prediction için feature set
    X_new = df_incomplete[features].copy()
    
    # Köşe tahmini (Over 8.5?)
    if model_corners is not None:
        prob_corners = model_corners.predict_proba(X_new)
        # prob_corners[:,0] = Under, prob_corners[:,1] = Over
        pred_corners = model_corners.predict(X_new)
    else:
        print("Korner modeli yok.")
        return

    # Kart tahmini (Over 2.5?)
    if model_cards is not None:
        prob_cards = model_cards.predict_proba(X_new)
        pred_cards = model_cards.predict(X_new)
    else:
        print("Kart modeli yok.")
        return

    # Sonuçları df_incomplete'a ekle
    df_incomplete["Pred_OverCorners8_5"] = pred_corners
    df_incomplete["Prob_UnderCorners8_5"] = prob_corners[:,0]
    df_incomplete["Prob_OverCorners8_5"] = prob_corners[:,1]

    df_incomplete["Pred_OverCards2_5"] = pred_cards
    df_incomplete["Prob_UnderCards2_5"] = prob_cards[:,0]
    df_incomplete["Prob_OverCards2_5"] = prob_cards[:,1]

    # Konsola yazdıralım
    for i, row in df_incomplete.iterrows():
        home, away = row["home_team_name"], row["away_team_name"]
        corner_pred = row["Pred_OverCorners8_5"]
        corner_prob_over = row["Prob_OverCorners8_5"]
        corner_prob_under = row["Prob_UnderCorners8_5"]
        card_pred = row["Pred_OverCards2_5"]
        card_prob_over = row["Prob_OverCards2_5"]
        card_prob_under = row["Prob_UnderCards2_5"]

        print(f"\n[TAHMİN] {home} vs {away} (MAÇ ID: {i})")
        print(f"  Köşe Over8.5 Tahmini: {corner_pred} (Under%={corner_prob_under*100:.2f}, Over%={corner_prob_over*100:.2f})")
        print(f"  Kart Over2.5 Tahmini: {card_pred} (Under%={card_prob_under*100:.2f}, Over%={card_prob_over*100:.2f})")

    return df_incomplete


def main(data_folder="deneme"):
    leagues = leagueselector(data_folder)
    if not leagues:
        print("Herhangi bir lig bulunamadı. Çıkılıyor...")
        return

    for league, paths in leagues.items():
        if "teams" not in paths or "matches" not in paths:
            print(f"{league} - 'teams' veya 'matches' dosyaları eksik.")
            continue

        print(f"\n=== {league.upper()} Ligi İşleniyor ===")
        df_teams = pd.read_csv(paths["teams"], encoding="utf-8-sig")
        df_matches = pd.read_csv(paths["matches"], encoding="utf-8-sig")

        # (A) Modelleri Eğit
        if "status" not in df_matches.columns:
            print("Matches CSV'de 'status' kolonunu bulamadım. Devam edemiyorum.")
            continue

        print("Model eğitimi başlıyor (köşe & kart)...")
        model_corners, model_cards, le_home, le_away, feat_cols, df_complete = train_corners_cards(df_matches)
        if model_corners is None or model_cards is None:
            print(f"{league} - Model eğitimi başarısız ya da sınıflar yetersiz.")
            continue

        # (B) Incomplete Maçlar İçin Tahmin
        print("\nYeni (incomplete) maç tahminleri:")
        df_incomplete_predictions = predict_incomplete_corners_cards(
            df_matches, model_corners, model_cards, le_home, le_away, feat_cols
        )

        # Dilerseniz tahmin sonuçlarını CSV olarak kaydedebilirsiniz
        if df_incomplete_predictions is not None and not df_incomplete_predictions.empty:
            df_incomplete_predictions.to_csv(f"{league}_incomplete_predictions.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    # Uygulama giriş noktası
    main(data_folder="deneme")
