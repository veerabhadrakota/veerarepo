from pydantic import BaseModel
from typing import Dict, Any

class WorkItemResponse(BaseModel):
    id: int
    fields: Dict[str, Any]

    class Config:
        extra = "allow"  # Let ADO return additional fields without errors