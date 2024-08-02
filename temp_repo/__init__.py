from nltk import download
from .mongodb.driver import init_db

def setup_environment():
    # Initialize database connection
    init_db()

    # Download necessary NLTK data
    download('stopwords')
    download('punkt')

setup_environment()