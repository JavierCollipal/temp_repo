
### Env file example: 
OPENAI_API_KEY=

### Init Stepes:
### Create a virtual environment:
python -m venv myenv

### Activate the virtual environment:
myenv\Scripts\Activate.ps1

### Intall dependencies:
pip install -r requirements.txt

### Data migration from xlsx:
1-Load Categories
python manage.py load_categories

2-Load Commerces
python manage.py load_commerces

3-Load Keywords
python manage.py load_keywords

4-Load Transactions
python manage.py load_transactions

### Local initialization:
python manage.py runserver

### About testing:
Unit testing applied on model and serializer, integration test applied on Views. 
# 100 enrichment with same description from provided data
python manage.py test temp_repo.tests.transactions.test_enrichhment_operation.EnrichmentOperationTestCase.test_enrichment_operation
# 1000 enrichment under 8 seconds 
python manage.py test temp_repo.tests.transactions.test_enrichment_operation.EnrichmentOperationTestCase.test_enrichment_operation temp_repo.tests.transactions.test_enrichment_operation.EnrichmentOperationTestCase.test_enrichment_performance_1000_transactions
