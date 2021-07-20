from pydantic import BaseModel


class BaseUser(BaseModel):
    login: str
    pswd: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
