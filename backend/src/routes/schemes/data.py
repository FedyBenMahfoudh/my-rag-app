from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional,List

class UploadRequest(BaseModel):
    files : List[UploadFile]


class ProcessRequest(BaseModel):
    file_id:Optional[str] = None

