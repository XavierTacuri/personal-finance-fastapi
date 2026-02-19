from fastapi import HTTPException
from app.models.db_models import User
from app.core.security import hash_password

class UserService:
    def __init__(self,repo):
        self.repo = repo

    def createUser(self,payload):
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=400,detail="Email already exists")

        user=User(
            name_user=payload.name_user,
            last_name=payload.last_name,
            email=payload.email,
            password_hash=hash_password(payload.password)
        )
        return self.repo.create(user)