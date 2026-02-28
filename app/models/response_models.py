# app/models/response_models.py

from pydantic import BaseModel
from typing import Optional

class OptionResponse(BaseModel):
    id: str
    title: str
    exchange: str
    expiry: Optional[str]
    entity_type: str