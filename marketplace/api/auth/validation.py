from pydantic import BaseModel, constr

class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"
