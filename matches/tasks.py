# betapp/matches/tasks.py
from celery import shared_task
from .betmodel.solo import get_betprogram_results
@shared_task
def update_betprogram_results():
    """
    Solo.py'deki hesaplama işlemini çalıştırarak veritabanını günceller.
    """
    results = get_betprogram_results()
    # İşlemin sonucu loglanabilir veya geri döndürülebilir.
    return results
