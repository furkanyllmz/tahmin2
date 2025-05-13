import os
import requests
from datetime import datetime,timedelta

API_KEY = os.getenv("RAPIDAPI_KEY")
BASE    = "https://v3.football.api-sports.io"
API_KEY = "a88105593e5fadb40037ec0d35244fee"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_finished_scores(date_str=None):
    """
    date_str: "YYYY-MM-DD" formatında; None ise bugün UTC tarihi kullanılır.
    döner: her biri bir maç objesi
    """
    if date_str is None:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    params = {
        "date": date_str,
        "status": "FT"   # sadece bitmiş maçlar
    }

    resp = requests.get(f"{BASE}/fixtures", headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    if "response" not in data:
        raise RuntimeError(f"API yanıtı beklenmedik: {data}")
    return data["response"]

if __name__ == "__main__":
    today = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    finished = get_finished_scores(today)
    print(f"✅ {today} tarihinde bitmiş {len(finished)} maçın skoru:")
    for m in finished:
        ht = m["teams"]["home"]["name"]
        at = m["teams"]["away"]["name"]
        score_h = m["goals"]["home"]
        score_a = m["goals"]["away"]
        league = m["league"]["name"]
        time = m["fixture"]["date"]  # ISO datetime
        print(f"  • [{league}] {ht} {score_h} - {score_a} {at}  (└ {time})")