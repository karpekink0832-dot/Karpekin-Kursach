from pydantic import BaseModel

class movietop(BaseModel):
    name: str
    id: int
    cost: int
    director: str

class User(BaseModel):
    username: str
    password: str