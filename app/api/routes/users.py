from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.user import userOut,user_Create
from app.repositories.users_repo import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

def get_service(db: Session = Depends(get_session)):
    return UserService(UserRepository(db))

@router.post("/", response_model=userOut,status_code=201)
def create_user(payload:user_Create, service: UserService = Depends(get_service)):
    return service.createUser(payload)
