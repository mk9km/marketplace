from datetime import datetime
from pydantic import BaseModel, constr

class EventCreateSchema(BaseModel):
    name: constr(min_length=3, max_length=64)
    date: datetime
    description: constr(min_length=10, max_length=128)


    class Config:
        extra = "forbid"
