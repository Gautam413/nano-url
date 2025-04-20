from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from urllib.parse import urlparse


class URLCreate(BaseModel):
    original_url: str
    creator_email: EmailStr
    authorized_emails: list[EmailStr]

    # @field_validator("original_url")
    # @classmethod
    # def validate_url(cls, value):
    #     parsed_url = urlparse(value)
    #     if not all([parsed_url.scheme, parsed_url.netloc]):  
    #         raise ValueError("Invalid URL: Must be a valid HTTP or HTTPS URL")
    #     return value  # ✅ Valid URL is returned unchanged

class AccessRequest(BaseModel):
    user_email: EmailStr
