from pydantic import BaseModel
from typing import List, Optional

class GetWorkItemRequest(BaseModel):
    project: str
    workItemId: int
    fields: Optional[List[str]] = None