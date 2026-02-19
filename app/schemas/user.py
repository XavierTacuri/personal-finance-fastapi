from pydantic import BaseModel, Field, EmailStr

class user_Create(BaseModel):
    name_user:str=Field(min_length=5,max_length=50)
    last_name:str=Field(min_length=5,max_length=50)
    email:EmailStr
    password:str =Field(min_length=8,max_length=18)

class userOut(BaseModel):
    id:int
    name_user:str
    last_name:str
    email:EmailStr

