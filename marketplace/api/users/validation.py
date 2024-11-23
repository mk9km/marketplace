from typing import Optional

from pydantic import BaseModel, constr

from marketplace.models import UserRole
from marketplace.models import UserState


class UserCreateSchema(BaseModel):
    username: constr(min_length=3, max_length=64)
    password: constr(min_length=8)
    role: Optional[UserRole] = UserRole.user
    state: Optional[UserState] = UserState.active

    class Config:
        extra = "forbid"

class UserModifySchema(BaseModel):
    password: constr(min_length=8)

    class Config:
        extra = "forbid"

class UserModifyByAdminSchema(BaseModel):
    password: constr(min_length=8)
    role: Optional[UserRole]
    state: Optional[UserState]

    class Config:
        extra = "forbid"