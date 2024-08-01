
### Env file example: 
OPENAI_API_KEY=

### Init Stepes:
### Create a virtual environment:
python -m venv myenv

### Activate the virtual environment:
myenv\Scripts\Activate.ps1

### Intall dependencies:
pip install -r requirements.txt

### Local initialization:
python manage.py migrate
python manage.py runserver

### About testing:
Unit testing applied on model and serializer, integration test applied on Views. 


python manage.py test temp_repo.tests
