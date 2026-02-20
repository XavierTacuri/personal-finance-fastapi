from app.core.security import hash_password, verify_password, create_access_token
from app.models.db_models import User
from app.repositories.users_repo import UserRepository


class AuthService:
    def __init__(self,users_repo:UserRepository):
        self.users_repo = users_repo

    def userRegister(self,name_user:str,last_name:str,email:str,password:str)->User:
        existing_user=self.users_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")

        user = User(
            name_user=name_user,
            last_name=last_name,
            email=email,
            password_hash=hash_password(password),
        )
        return self.users_repo.userCreate(user)

    def login(self,email:str,password:str)->str:
        user=self.users_repo.get_by_email(email)
        if not user or not verify_password(password,user.password_hash):
            raise ValueError("Invalid Credentials")

        return create_access_token(subject=str(user.id))

