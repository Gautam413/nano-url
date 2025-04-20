from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os

# Load environment variables from .env

#DATABASE_URL="postgresql://postgres.nllpdwffmmqvswhcjmfa:WNLYtxLM6pVLJ33w@aws-0-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require"

load_dotenv()
print("Loaded DATABASE_URL:", os.getenv("DATABASE_URL"))  # Debugging line

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)

    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW();"))  # ✅ FIXED HERE
        print("✅ Database Connection Successful:", result.fetchone())
except Exception as e:
    print("❌ Database Connection Failed:", e)


