from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session


from app.core.config import settings
from app.db.session import get_session
from app.repositories.users_repo import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401,detail="Ivalid token")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401,detail="Invalid token")

    user= UserRepository(db).get_ID(user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user