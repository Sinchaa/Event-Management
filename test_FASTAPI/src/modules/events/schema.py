from pydantic import BaseModel,Field

from datetime import datetime



class CreateEventRequest(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        orm_mode = True


# class UpdateUserRequest(BaseModel):
#     name: str
#     email: str
#     eff_status:str = Field(max_length = 1)
#     dataprfl:str
#     oprid:str
#     emplid:str
#     effdt: date
#     dataprfl: str

#     class Config:
#         orm_mode = True