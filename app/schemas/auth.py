from pydantic import BaseModel,Field,EmailStr

class userRegister(BaseModel):
    name_user: str=Field(min_length=2,max_length=50)
    last_name: str=Field(min_length=2,max_length=50)
    email: EmailStr
    password: str=Field(min_length=8,max_length=20)

class userLogin(BaseModel):
    email: EmailStr
    password: str

class tokenOut(BaseModel):
    access_token: str
    token_type: str="Bearer"

