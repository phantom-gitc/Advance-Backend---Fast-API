from sqlmodel import SQLModel , Session , create_engine


DATABASE_URL = "sqlite:///rangmanch.db"
engine = create_engine(DATABASE_URL , echo=True)




# Function To Create Tables (When Server Starts)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Function To Get Session (Through Dependency Injection)

def get_session():  
    with Session(engine) as session:
        yield session