# Pydantinc
# Python
from datetime import datetime
from typing import Optional
from uuid import UUID
# Pydantinc
from pydantic import BaseModel, Field, Required
# Custom
from models.users import User


class Tweet(BaseModel):
    tweet_id: UUID = Field(Required)
    content: str = Field(
        Required,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(defualt=None)
    by: User = Field(Required)
