import os
import logging
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

Base = declarative_base()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL is not set. Please check your .env file.")
    raise ValueError("DATABASE_URL is missing!")

# Create async engine
try:
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)
    logger.info("Database engine created successfully.")
except SQLAlchemyError as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# Create session factory
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dependency to get a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            logger.info("Database session created successfully.")
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()
            logger.info("Database session closed.")

