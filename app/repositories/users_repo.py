from sqlmodel import Session, select
from app.models.db_models import User

class UserRepository:
    def __init__(self,db:Session):
        self.db = db

    def get_by_email(self,email:str):
        stmt = select(User).where(User.email==email)
        return self.db.exec(stmt).first()

    def get_ID(self,user_id:int):
        return self.db.get(User,user_id)

    def userCreate(self,user:User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
