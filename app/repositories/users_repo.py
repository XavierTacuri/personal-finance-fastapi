from sqlmodel import Session, select
from app.models.db_models import User

class UserRepository:
    def __init__(self,db:Session):
        self.db = db

    def get_by_email(self,email:str):
        return self.db.execute(select(User).where(User.email == email)).first()

    def create(self,user:User)->User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
