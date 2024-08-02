import json
from uuid import UUID
from django.core.management.base import BaseCommand
from temp_repo.models.category import Category

class Command(BaseCommand):
    help = 'Load categories data into MongoDB'

    def handle(self, *args, **options):
        with open('data/initial_data/categorias.json', 'r') as file:
            categories = json.load(file)
            for category in categories:
                # Convert the ID string to a UUID object
                category_id = UUID(category['id'])
                Category(
                    id=category_id,  # Use UUID object for the id field
                    name=category['name'],
                    type=category['type']
                ).save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded categories data'))
