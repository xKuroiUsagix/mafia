from pydantic import BaseModel, EmailStr, StringConstraints


class UserBase(BaseModel):
    username: str = StringConstraints(max_length=128)
    email: EmailStr = StringConstraints(max_length=256)

class UserCreateRequest(UserBase):
    password: str = StringConstraints(max_length=64)
    confirm_password: str = StringConstraints(max_length=64)

class UserResponse(UserBase):
    id: int

class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
