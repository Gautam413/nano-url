from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta

class ShortURL(Base):
    __tablename__ = "short_urls"
    
    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    creator_email = Column(String, nullable=False)
    authorized_emails = Column(String, nullable=False)  # Comma-separated
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=60))

class AccessLog(Base):
    # __tablename__ = "access_logs"

    # id = Column(String, primary_key=True, index=True)
    # short_url = Column(String, nullable=False)
    # user_email = Column(String, nullable=False)
    # accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Changed to Integer
    short_url = Column(String, nullable=False)
    accessed_by = Column(String, nullable=False)
    accessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# class VerificationToken(Base):
#     __tablename__ = "verification_tokens"

#     token = Column(String, primary_key=True, index=True)
#     user_email = Column(String, nullable=False)
#     short_url = Column(String, nullable=False)
#     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
#     expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=0.00208333))