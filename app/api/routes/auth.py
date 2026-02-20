from os import name

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.auth import userRegister,userLogin,tokenOut
from app.repositories.users_repo import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",status_code=201)
def userRegister(payload:userRegister,db:Session=Depends(get_session)):
    try:
        user=AuthService(UserRepository(db)).userRegister(
            name_user=payload.name_user,
            last_name=payload.last_name,
            email=payload.email,
            password=payload.password,
        )
        return {"id":user.id, "name":user.name_user,"last_name":user.last_name, "email":user.email}
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/login",response_model=tokenOut)
def login(payload:userLogin,db:Session=Depends(get_session)):
    try:
        token=AuthService(UserRepository(db)).login(
            payload.email,
            payload.password
        )
        return tokenOut(access_token=token)
    except ValueError:
        raise HTTPException(status_code=400,detail="Incorrect email or password")