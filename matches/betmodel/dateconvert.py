
import locale
from datetime import datetime,timedelta

MONTHS_TR = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan",
    "05": "Mayıs", "06": "Haziran", "07": "Temmuz", "08": "Ağustos",
    "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"
}


def parse_date_only(date_str):
    """
    Bu fonksiyon, verilen tarih stringini "YYYY-MM-DD" formatına dönüştürür.
    
    Eğer giriş:
      - ISO formatında ise (örneğin: "2025-02-28"), onu direkt döndürür.
      - Alternatif formatta ise (örneğin: "Feb 14 2025 - 8:00pm"), onu parse edip "YYYY-MM-DD" olarak döndürür.
    """
    try:
        # Önce ISO formatını dene
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            # ISO formatında değilse, alternatif formatı dene
            dt = datetime.strptime(date_str, "%b %d %Y - %I:%M%p")
        except ValueError:
            raise ValueError(f"Tarih formatı desteklenmiyor: {date_str}")
    return dt.strftime("%Y-%m-%d")

def get_time(time_str):
    """
    Bu fonksiyon, verilen zaman stringini "HH:MM" (24 saat) formatına dönüştürür.
    
    Eğer giriş:
      - "HH:MM" formatında ise, direkt döndürür (örneğin: "20:00").
      - 12 saatlik formatta ise (örneğin: "8:00pm"), 24 saatlik formata çevirir.
    """
    try:
        # Önce 24 saatlik formatı dene
        dt = datetime.strptime(time_str, "%H:%M")
    except ValueError:
        try:
            # 12 saatlik formatı dene
            dt = datetime.strptime(time_str.upper(), "%I:%M%p")
        except ValueError:
            raise ValueError(f"Zaman formatı desteklenmiyor: {time_str}")
    return dt.strftime("%H:%M")


