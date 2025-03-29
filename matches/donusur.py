import csv
import uuid
from datetime import datetime
import re
import hashlib

def slugify_team_name(name):
    # Basit bir slugify örneği
    s = name.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


from datetime import datetime

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


# Örnek kullanım
raw_date = "Feb 14 2025 - 8:00pm"
parsed_date = parse_date_only(raw_date)
print(parsed_date)  # "2025-02-14"

def generate_stable_id(home_team, away_team,):
    """
    Ev sahibi takım, deplasman takımı ve tarih bilgisine göre sabit bir hash (id) üretir.
    """
    unique_str = home_team + away_team 
    # MD5 hash'ini hesapla ve ilk 8 karakterini kullan (isteğe bağlı, uzunluğu ayarlayabilirsiniz)
    return hashlib.md5(unique_str.encode('utf-8')).hexdigest()[:8]

def read_csv_to_match_list(csv_file_path):
    match_list = []
    
    # CSV'yi oku
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # corner_prediction: "Over 8.5" => 1, aksi halde 0
            home_team = row["HomeTeam"].strip()
            away_team = row["AwayTeam"].strip()
            home_slug = slugify_team_name(home_team)
            away_slug = slugify_team_name(away_team)
            stable_id = generate_stable_id(home_team, away_team,)
            
            # Tek satırdan match_dict'i oluştur
            match_dict = {
                "id":stable_id,
                "home_team": home_team,
                "away_team": away_team,
                "home_team_wins":row["MS1"],
                "no_wins":row["MSX"],
                "away_team_wins":row["MS2"],
                "KG": row["KG VAR"],
                "over2_5":row["OVER2.5"],
                "home_team_logo":  f"{home_slug}.png",
                "away_team_logo": f"{away_slug}.png",
                "match_date":parse_date_only(row["DATE"].strip()),
                


            }    
            
            match_list.append(match_dict)
            
    
    return match_list

# Fonksiyonu kullanma örneği
if __name__ == "__main__":
    
    
    csv_file = "stats/england-premier-league_results.csv"  # CSV dosya adınızı/konumunuzu buraya yazın
    match_list = read_csv_to_match_list(csv_file)
    
    # Elde edilen match_list'i yazdıralım
    for match in match_list:
        print(match["id"])
        
