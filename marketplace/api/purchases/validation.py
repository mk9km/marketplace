from pydantic import BaseModel, Field, constr


class PurchaseCreateSchema(BaseModel):
    ticket_id: int
    quantity: int = Field(..., gt=0)

    class Config:
        extra = "forbid"
