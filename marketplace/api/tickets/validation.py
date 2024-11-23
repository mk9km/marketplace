from pydantic import BaseModel, Field, constr


class TicketCreateSchema(BaseModel):
    name: constr(min_length=3, max_length=64)
    event_id: int
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

    class Config:
        extra = "forbid"
