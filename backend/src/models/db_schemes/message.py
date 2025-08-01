from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
import datetime
from ..enums.MessageRoleEnum import MessageRoleEnum

class Message(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    content: str
    role: str
    createdAt: Optional[datetime.datetime] = None
    updatedAt: Optional[datetime.datetime] = None
    conversation_id: ObjectId

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("conversation_id", 1)],
                "name": "conversation_id_index",
                "unique": False
            },
            {
                "key": [("conversation_id", 1), ("created_at", -1)],
                "name": "conversation_id_created_at_index",
                "unique": False
            }
        ]
