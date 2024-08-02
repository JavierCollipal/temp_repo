### Follow the steps in order for local:
### Create a virtual environment:
python -m venv myenv

### Activate the virtual environment:
myenv\Scripts\Activate.ps1

### Intall dependencies:
pip install -r requirements.txt

### Data migration from xlsx:
python manage.py load_everything

### Local initialization:
python manage.py runserver
or
python manage.py test temp_repo.tests

### About testing:
integration test applied on every CRUD. 
# test all the folders
 python manage.py test temp_repo.tests

# 1000 enrichment under 8 seconds; doesn't work
python manage.py test temp_repo.tests.transactions.test_enrichment_operation.EnrichmentOperationTestCase.test_enrichment_operation temp_repo.tests.transactions.test_enrichment_operation.EnrichmentOperationTestCase.test_enrichment_performance_1000_transactions


###Enrichment process:
An atlas text search is being made on every keyword search with the transaction  description.
