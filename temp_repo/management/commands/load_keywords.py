import json
from uuid import UUID
from django.core.management.base import BaseCommand
from temp_repo.models.keyword import Keyword
from temp_repo.models.commerce import Commerce

class Command(BaseCommand):
    help = 'Load keyword data into MongoDB'

    def handle(self, *args, **options):
        with open('data/initial_data/keywords.json', 'r') as file:
            keywords = json.load(file)
            for keyword_data in keywords:
                try:
                    # Check if merchant_id is valid and not NaN/None
                    merchant_id = keyword_data.get('merchant_id')
                    if merchant_id and not (merchant_id is None or (isinstance(merchant_id, float) and math.isnan(merchant_id))):
                        # Convert merchant_id to UUID object
                        merchant_id = UUID(merchant_id)
                        # Fetch the corresponding Commerce document
                        merchant = Commerce.objects(id=merchant_id).first()
                    else:
                        merchant = None

                    if merchant:
                        # Create and save the Keyword document
                        Keyword(
                            id=UUID(keyword_data['id']),  # Convert string to UUID
                            keyword=keyword_data['keyword'],
                            merchant_id=merchant
                        ).save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully loaded keyword: {keyword_data["keyword"]}'))
                    else:
                        self.stderr.write(self.style.ERROR(f'Merchant not found for ID: {keyword_data["merchant_id"]}'))

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error loading keyword: {keyword_data["keyword"]}, Error: {str(e)}'))