from .mongodb.driver import init_db

def setup_environment():
    # Initialize database connection
    init_db()

setup_environment()