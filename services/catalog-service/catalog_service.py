from catalog_repository import ProductRepository
from models import Product
from schemas import ProductCreate, ProductUpdate
import uuid

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data: ProductCreate) -> Product:
        product = Product(
            id = uuid.uuid4(),
            name = data.name,
            description = data.description,
            price = data.price,
            stock = data.stock,
            category = data.category
        )
        return self.repo.create(product)

    def get_product(self, product_id: str) -> Product | None:
        return self.repo.get_by_id(product_id)

    def get_products(self):
        return self.repo.get_all()

    def update_products(self, product_id: str, data: ProductUpdate) -> Product | None: 
        product = self.repo.get_by_id(product_id)
        if not product:
            return None
        update_data = data.model_dump(exclude_unset=True) # exclude_unset=True - не включать поля которые переданы не явно
        return self.repo.update(product, update_data)

    def delete_product(self, product_id: str) -> bool:
        product = self.repo.get_by_id(product_id)
        if not product:
            return False
        self.repo.delete(product)
        return True