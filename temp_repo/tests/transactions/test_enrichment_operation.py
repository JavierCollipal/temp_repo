from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from temp_repo.models.transaction import Transaction
from datetime import datetime
import random
import time

class EnrichmentOperationTestCase(APITestCase):
    def setUp(self):
        print("\n[Setup] Preparing data for enrichment operation tests...")
        self.url = reverse('enrichment-operation')

        # List of descriptions to be used for the transactions
        self.transaction_descriptions = [
            "PETROBRAS 11 ORTE/7 SU", "PETROBRAS 9 NTE/7 ORNTE", "PETROBRAS AEROPUERTO",
            "PETROBRAS ALTO HOSPIC", "PEDIDOSYA 3D RESTAURANT", "PEDIDOSYA 3D SUPERMERC",
            "PEDIDOSYA INDUMENT RIDERS", "PEDIDOSYA MARKETS 9262", "PEDIDOSYA PROPINA",
            "McDonalds Las Condes", "FACEBK 85ENTJXAQ2", "FACEBK 85GSQFKH92",
            "FACEBK 85R97HKYG2", "SumUp *DOMINOS PIZZA G", "PAYPAL *DOMINOS",
            "DOMINO S PIZZA", "Domino s Pizza Frederi", "DOMINO S PIZZA LA 10",
            "DOMINO SANTA ROSA", "DOMINO'S 2080", "DOMINO'S 2759", "DOMINO'S 3232",
            "DOMINO'S 3684", "DOMINO'S 4342", "SALCOBRAND 433 JUMBO C",
            "SALCOBRAND 433 JUMBO CALA", "CRUZVERDE CV 9059", "CRUZVERDE CV 9060",
            "CRUZVERDE CV 9061", "CRUZVERDE CV9081", "CRUZVERDE CV9087",
            "C. VERDE JUMBO RANCAGUA", "C. VERDE JUMBO V DEL M", "C. VERDE JUMBO V DEL MAR",
            "merpago aguasandinas", "UNIRED CL AGUAS ANDINAS", "AGUAS ANDINAS",
            "AGUAS ANDINAS ONEPAY", "MCB 02 AGUAS ANDINAS", "COMPRA NACIONAL EASY LA DEHESA",
            "Compra Nacional EASY RANCAGUA", "EASY ALTO LAS CONDE", "EASY ALTO LAS CONDES",
            "EASY ANTOFAGASTA", "EASY CALAMA", "EASY CERRILLOS", "EASY CHIGUAYANTE",
            "EASY CHILLAN", "EASY CONCHA Y TORO", "EXPRESS - LIDER",
            "EXPRESS - LIDER CONCE", "EXPRESS - LIDER CONCE TRE", "EXPRESS ALGARROBO",
            "EXPRESS ANDINO", "EXPRESS ANDRNS MELLADO", "EXPRESS ANGELINO",
            "EXPRESS ANTOFAG PEREZ", "EXPRESS BUIN SAN MARTIN", "EXPRESS BUIN SAN MARTIN",
            "EXPRESS CIUD DE LOS VA", "EXPRESS CIUD DE LOS VALLE", "EXPRESS CIUDAD DE BARCELO",
            "EXPRESS CIUDAD DEL ES", "MP *RECARGA BIP]", "MP *RECARGA BIP|",
            "BC UBER CASH", "PAYPAL *UBER", "PAYPAL *UBER BR", "PAYPAL *UBER BV",
            "PAYPAL *UBERPAYMENT", "PAYU *UBER TR", "PAYU-UBER 828987",
            "PAYPAL *UBER EATS", "PAYPAL *UBERBV EATS", "PAYPAL *UBEREATS AU",
            "UBER *EATS HELP.UBER.C", "UBER *EATS HELP.UBER.C", "UBER *EATS HELP.UBER.COM",
            "UBER CANADA/UBEREATS", "UBER EATS", "UBER EATS", "UBER* EATS", "UBER* EATS",
            "UNDER AMOUR MALL PLAZA VE", "UNDER ARMOUR", "UNDER ARMOUR CANCUN IC",
            "Pago TDC ITAU", "Pago TDC ITAU", "Pago TDC ITAU", "Pago TDC ITAU",
            "BOLT", "UNIMARC - COORONEL", "UNIMARC ANDALUE (CABRERO)",
            "UNIMARC ANGOL I", "UNIMARC ANTOFAGASTA", "UNIMARC ARAUCO", "UNIMARC ATACAMA",
            "UNIMARC AV ESPANA"
        ]

        # Generate transaction data without saving them in the database
        self.transaction_data = [
            {
                'description': self.transaction_descriptions[i % len(self.transaction_descriptions)],
                'amount': round(random.uniform(-9999.99, 9999.99), 2),  # Ensure total digits <= 10
                'date': datetime.now().strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
            }
            for i in range(100)
        ]

    def test_enrichment_operation(self):
        print("[TEST] Performing enrichment operation on transactions.")

        # Simulate a REST call with transaction-like objects
        response = self.client.post(self.url, {'transactions': self.transaction_data}, format='json')

        # Check for successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}")

        response_data = response.json()
        
        # Check for metrics in the response data
        self.assertIn('categorization_rate', response_data, "Categorization rate is missing in response data.")
        self.assertIn('merchant_identification_rate', response_data, "Merchant identification rate is missing in response data.")
        self.assertIn('match_keyword_rate', response_data, "Match keyword rate is missing in response data.")

    def test_enrichment_performance_1000_transactions(self):
        print("[TEST] Performance test for enriching 1000 transactions.")

        # Generate 1000 transaction data (first 100 from descriptions, rest random)
        transaction_data = [
            {
                'description': self.transaction_descriptions[i % len(self.transaction_descriptions)],
                'amount': round(random.uniform(-9999.99, 9999.99), 2),
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            for i in range(1000)
        ]

        # Measure the time taken for the enrichment process
        start_time = time.time()
        response = self.client.post(self.url, {'transactions': transaction_data}, format='json')
        end_time = time.time()

        duration = end_time - start_time
        print(f"Enrichment process took {duration:.2f} seconds")

        # Check if the response time is within the 8-second limit
        self.assertTrue(duration < 8, f"Enrichment took too long: {duration} seconds")

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"Expected status code 200, got {response.status_code}")