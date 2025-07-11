from typing import List
from pydantic import BaseModel, Field


class BulkResponseFailure(BaseModel):
    id: int
    error: str

class BulkResponse(BaseModel):
    success_count: int
    failures: List[BulkResponseFailure]


