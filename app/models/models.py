from pydantic import BaseModel

class movietop(BaseModel):
    name: str
    id: int
    cost: int
    director: str
