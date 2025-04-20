# alembic/env.py
import sys
import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

#sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base  # Import your SQLAlchemy models

from dotenv import load_dotenv

# Load environment variables
#load_dotenv(dotenv_path="C:/Users/devte/Desktop/urk/.env")
# Load environment variables from .env
load_dotenv()

# Replace sqlalchemy.url with DATABASE_URL from .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    context.config.set_main_option("sqlalchemy.url", db_url)

# Get the DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file!")

print(f"Original DATABASE_URL: {DATABASE_URL}") # Debugging

config = context.config

# --- Prepare Synchronous URL for Alembic ---
# Store the original async URL if needed elsewhere, but derive the sync one
ASYNC_DATABASE_URL = DATABASE_URL
SYNC_DATABASE_URL = None

if ASYNC_DATABASE_URL.startswith("postgresql+asyncpg"):
    SYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    # Install psycopg2 if you haven't: pip install psycopg2-binary
elif ASYNC_DATABASE_URL.startswith("postgresql"): # Already sync
    SYNC_DATABASE_URL = ASYNC_DATABASE_URL
else:
    # Handle other potential database types if necessary
    SYNC_DATABASE_URL = ASYNC_DATABASE_URL # Assume sync if not asyncpg

if not SYNC_DATABASE_URL:
     raise ValueError("Could not determine a synchronous DATABASE_URL for Alembic.")

print(f"Synchronous URL for Alembic: {SYNC_DATABASE_URL}") # Debugging

# Set the *synchronous* database URL in alembic config
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# Make sure 'models' can be imported from the alembic directory's perspective
# You might need to adjust Python path or use relative imports if 'models.py'
# is not in the root or directly accessible.
target_metadata = Base.metadata

# --- Offline Mode ---
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # url = config.get_main_option("sqlalchemy.url") # Already uses the sync url set above
    url = SYNC_DATABASE_URL # Or directly use the variable
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# --- Online Mode (Corrected) ---
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use the synchronous URL derived earlier to create a synchronous engine
    # Alembic needs a sync connection even if your app is async
    connectable = create_engine(SYNC_DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
            # include_schemas=True # Add this if you use schemas like 'public' explicitly
        )
        # Use transaction.begin() for non-transactional DDL support (optional)
        with context.begin_transaction():
            context.run_migrations()

# --- Execution Logic ---
if context.is_offline_mode():
    print("Running migrations offline...")
    run_migrations_offline()
else:
    print("Running migrations online...")
    run_migrations_online()

print("env.py execution finished.")