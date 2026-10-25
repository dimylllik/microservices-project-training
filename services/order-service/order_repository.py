from sqlalchemy.orm import Session
from models import Order

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: str) -> Order | None:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_user_orders(self,user_id: str) -> list[Order]:
        return self.db.query(Order).filter(Order.user_id == user_id).all()

    def cancel_order(self, order_id: str):
        order = self.get_order(order_id)

        if order is None:
            return None

        if  order.status == "PENDING":
            order.status = "CANCELLED"
            self.db.commit()
            self.db.refresh(order)
        
        return order
            
    def mark_order_paid(): # обработка успешной оплаты (сделать после рэбита)
        pass

    def mark_order_failed(): # обработка неуспешной оплаты (сделать после рэбита)
        pass