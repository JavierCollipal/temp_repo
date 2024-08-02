from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load all data in the specified order'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data loading process...'))
        
        call_command('load_categories')
        self.stdout.write(self.style.SUCCESS('Categories loaded successfully.'))
        
        call_command('load_commerces')
        self.stdout.write(self.style.SUCCESS('Commerces loaded successfully.'))
        
        call_command('load_keywords')
        self.stdout.write(self.style.SUCCESS('Keywords loaded successfully.'))
        
        call_command('load_transactions')
        self.stdout.write(self.style.SUCCESS('Transactions loaded successfully.'))
        
        self.stdout.write(self.style.SUCCESS('All data loaded successfully.'))
