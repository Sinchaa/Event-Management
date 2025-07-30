from pydantic import BaseModel

class CreateAttendeeRequest(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
