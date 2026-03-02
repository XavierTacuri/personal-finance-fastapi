from fastapi import APIRouter,Depends
from sqlmodel import Session
from app.api.deps import get_session, get_current_user
from app.repositories.categories_repo import CategoryRepository
from app.schemas.category import Category, CategoryOut
from app.services.category_service import CategoryService
from typing import List

router = APIRouter(prefix="/categories",tags=["categories"])

@router.post("",response_model=Category,status_code=201)
def createCategory(payload:Category,
                   db: Session = Depends(get_session),
                    user=Depends(get_current_user)):
    service = CategoryService(CategoryRepository(db))
    return service.createCategory(user_id=user.id,payload=payload)

@router.get(path="", response_model=List[CategoryOut])
def listCategories(
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    service = CategoryService(CategoryRepository(db))
    return service.listCategories(user_id=user.id)
