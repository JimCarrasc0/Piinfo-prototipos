from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config(".env")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}"
    f"@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,   # evita ERROR: server closed the connection unexpectedly
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
