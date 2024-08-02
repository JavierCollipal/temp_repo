import json
from uuid import UUID
from django.core.management.base import BaseCommand
from temp_repo.models.commerce import Commerce
from temp_repo.models.category import Category
import math

class Command(BaseCommand):
    help = 'Load commerce data into MongoDB'

    def handle(self, *args, **options):
        with open('data/initial_data/comercios.json', 'r') as file:
            commerces = json.load(file)
            for commerce in commerces:
                try:
                    # Check if category_id is valid and not NaN/None
                    category_id = commerce.get('category_id')
                    if category_id and not (category_id is None or (isinstance(category_id, float) and math.isnan(category_id))):
                        # Convert category_id to UUID object
                        category_id = UUID(category_id)
                        # Fetch the corresponding Category document
                        category = Category.objects(id=category_id).first()
                    else:
                        category = None

                    # Check if merchant_logo is valid and not NaN/None
                    merchant_logo = commerce.get('merchant_logo')
                    if merchant_logo and not (merchant_logo is None or (isinstance(merchant_logo, float) and math.isnan(merchant_logo))):
                        merchant_logo = str(merchant_logo)
                    else:
                        merchant_logo = None

                    # Create and save the Commerce document
                    Commerce(
                        id=UUID(commerce['id']),  # Convert string to UUID
                        merchant_name=commerce['merchant_name'],
                        merchant_logo=merchant_logo,  # Only set if it's valid
                        category=category  # Can be None if not found
                    ).save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded commerce: {commerce["merchant_name"]}'))

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error loading commerce: {commerce["merchant_name"]}, Error: {str(e)}'))