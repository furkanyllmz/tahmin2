from django.core.management.base import BaseCommand
from datetime import date, timedelta
from matches.models import MatchResult

class Command(BaseCommand):
    help = 'Bugünün tarihinden 3 gün öncesine kadar olan kayıtları siler.'

    def handle(self, *args, **options):
        cutoff_date = date.today() - timedelta(days=3)
        
        deleted_count,_=MatchResult.objects.all().delete()
        self.stdout.write(f"{deleted_count} kayıt silindi.")
