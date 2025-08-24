from pydantic import EmailStr, BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role : str

# For reading user details (responses)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    # is_admin: Optional[bool] = False

    class Config:
        orm_mode = True