from sqlalchemy import create_engine

# Connect to database using sql alchemy its localeted in ./data/aidence.db

def create_db_connection(database_url = "sqlite:///./data/aidence.db"):
    # Create the SQLAlchemy engine
    engine = create_engine(database_url)
    return engine