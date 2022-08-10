from pydantic import BaseModel, constr, EmailStr, validator, ValidationError


class BaseUser(BaseModel):
    email: EmailStr
    username: constr(max_length=120)


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
