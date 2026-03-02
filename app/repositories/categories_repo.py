from sqlmodel import Session,select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.db_models import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db=db

    def createCategoery(self,user_id: int,name: str)->Category:
        category = Category(user_id=user_id,name=name)

        try:
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400,detail="Category already exists")

    def get_all(self, user_id: int):
        stmt = select(Category).where(Category.user_id == user_id)
        return self.db.exec(stmt).all()