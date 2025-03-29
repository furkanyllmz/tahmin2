from django import template
from datetime import datetime,date

register = template.Library()

@register.filter
def to_turkish_date(value):
    """
    ISO formatındaki tarihi "Gün Ay" formatına çevirir.
    Örneğin: "2025-02-24" -> "24 Şubat"
    """
    try:
        dt = datetime.strptime(value, "%Y-%m-%d").date()
        if dt==date.today():
            return "Bugün"
        aylar = {
            1: "Ocak",
            2: "Şubat",
            3: "Mart",
            4: "Nisan",
            5: "Mayıs",
            6: "Haziran",
            7: "Temmuz",
            8: "Ağustos",
            9: "Eylül",
            10: "Ekim",
            11: "Kasım",
            12: "Aralık"
        }
        return f"{dt.day} {aylar.get(dt.month, '')}"
    except Exception as e:
        return value  # Hata olursa orijinal değeri döndür

