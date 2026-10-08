from sqlalchemy.orm import Session
from models import Order

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order():
        pass
    