
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
