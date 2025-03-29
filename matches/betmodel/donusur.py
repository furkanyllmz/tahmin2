import csv


def read_csv_to_match_list(csv_file_path):
    match_list = []
    
    # CSV'yi oku
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # corner_prediction: "Over 8.5" => 1, aksi halde 0
            
            
            # Tek satırdan match_dict'i oluştur
            match_dict = {
                "home_team": row['HomeTeam'],
                "away_team": row['AwayTeam'],
                "home_team_wins":row["MS1"],
                "no_wins":row["MSX"],
                "away_team_wins":row["MS2"],
                "KG": row["KG VAR"],
                "over2.5":row["OVER2.5"],
            }
            
            match_list.append(match_dict)
    
    return match_list

# Fonksiyonu kullanma örneği
if __name__ == "__main__":
    csv_file = "europe-uefa-europa-league_results.csv"  # CSV dosya adınızı/konumunuzu buraya yazın
    match_list = read_csv_to_match_list(csv_file)
    
    # Elde edilen match_list'i yazdıralım
    for match in match_list:
        print(match)
