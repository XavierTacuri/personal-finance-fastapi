from app.repositories.categories_repo import CategoryRepository
from app.schemas.category import Category


class CategoryService:
    def __init__(self, repo:CategoryRepository):
        self.repo = repo

    def createCategory(self,user_id:int, payload:Category):
        return self.repo.createCategoery(user_id=user_id,name=payload.name)

