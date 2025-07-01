from datetime import datetime
from pydantic import BaseModel


class BackupOut(BaseModel):
    filename: str
    size_mb: float
    created_at: datetime
    status: str = "success"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
