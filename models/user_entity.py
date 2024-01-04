from pydantic import BaseModel
#from typing import Optional

class User(BaseModel):
    id: str | None
    username: str
    email: str