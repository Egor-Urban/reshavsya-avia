# backend/database.py



from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



DB_PATH = Path(__file__).parent / "data" / "app.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()



def get_db():
    db = Session()
    
    try:
        yield db
        
    finally:
        db.close()