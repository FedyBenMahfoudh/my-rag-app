from pydantic import BaseModel
from typing import Optional

class PushRequest(BaseModel):
    do_reset: Optional[int] = 1

class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 5
    chat_history: list[object] = []  # list of {"content": ..., "role": ...}
