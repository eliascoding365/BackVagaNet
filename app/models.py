from pydantic import BaseModel


class Vaga(BaseModel):
    description: str
    name: str


# class User(BaseModel):
#     name: str
#     email: str
#     password: str


