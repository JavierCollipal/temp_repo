# management/commands/load_transactions.py
import json
from uuid import UUID
from django.core.management.base import BaseCommand
from temp_repo.models.transaction import Transaction
from datetime import datetime, timedelta
import math
import random

class Command(BaseCommand):
    help = 'Load transaction data into MongoDB'

    def handle(self, *args, **options):
        with open('data/initial_data/transacciones.json', 'r') as file:
            transactions = json.load(file)
            for transaction_data in transactions:
                try:
                    # Handle amount: If None or NaN, assign a random value
                    amount = transaction_data.get('amount')
                    if amount is None or (isinstance(amount, float) and math.isnan(amount)):
                        # Generate a random amount between -1000 and 1000, half positive, half negative
                        amount = random.uniform(-1000, 1000)

                    # Handle date: If None or NaN, assign a random date
                    date_str = transaction_data.get('date')
                    if date_str is None or (isinstance(date_str, float) and math.isnan(date_str)):
                        # Generate a random date within the past year
                        start_date = datetime.now() - timedelta(days=365)
                        date = start_date + timedelta(days=random.randint(0, 365))
                    else:
                        date = datetime.strptime(date_str, "%Y-%m-%d")

                    # Create and save the Transaction document
                    Transaction(
                        id=UUID(transaction_data['id']),  # Convert string to UUID
                        description=transaction_data['description'],
                        amount=amount,
                        date=date
                    ).save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded transaction: {transaction_data["description"]}'))

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error loading transaction: {transaction_data["description"]}, Error: {str(e)}'))