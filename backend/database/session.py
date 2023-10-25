from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config


def get_session(config: Config) -> Session:
    engine = create_engine(
        config.postgres_url,
        pool_size=30,
        max_overflow=0,
        pool_pre_ping=True,  # liveness upon each checkout
    )

    with Session(engine) as session:
        try:
            yield session
            session.commit()
        finally:
            session.rollback()
