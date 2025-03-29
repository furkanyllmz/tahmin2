# betapp/management/commands/update_betresults.py

from django.core.management.base import BaseCommand
from matches.betmodel.solo import get_data_from_db

class Command(BaseCommand):
    help = 'Tek seferlik olarak CSV dosyalarından veritabanına veri yazar.'

    def handle(self, *args, **options):
        self.stdout.write("Hesaplama işlemi başlıyor...")
        results = get_data_from_db()
        self.stdout.write("İşlem tamamlandı, veriler veritabanına kaydedildi.")
