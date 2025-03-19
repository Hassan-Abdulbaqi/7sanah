from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Populates the database with all Hijri months and their events'

    def handle(self, *args, **options):
        # Call individual month population commands
        self.stdout.write(self.style.SUCCESS('Starting to populate Hijri calendar...'))
        
        # Populate Muharram
        self.stdout.write(self.style.SUCCESS('\nPopulating Muharram...'))
        call_command('populate_muharram')
        
        # Populate Safar
        self.stdout.write(self.style.SUCCESS('\nPopulating Safar...'))
        call_command('populate_safar')
        
        # Add more months as they are implemented
        # call_command('populate_rabi_al_awwal')
        # call_command('populate_rabi_al_thani')
        # etc.
        
        self.stdout.write(self.style.SUCCESS('\nHijri calendar population completed successfully!')) 