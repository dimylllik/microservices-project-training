from order_repository import OrderRepository
from models import Order, OrderItem
from schemas import OrderCreate
from uuid import UUID

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, data: OrderCreate) -> Order:
        items = []
        total = 0

        for item_data in data.items:
            item = OrderItem(
                product_id= item_data.product_id,
                quantity= item_data.quantity,
                price= item_data.price
            )
            items.append(item)
            total += item_data.quantity * item_data.price

        order = Order(
            user_id = data.user_id,
            total = total,
            items = items 
        )

        return self.repo.create_order(order)

    def get_order(self, order_id: UUID) -> Order | None:
        return self.repo.get_order(order_id)

    def get_user_orders(self, user_id: UUID) -> list[Order]:
        return self.repo.get_user_orders(user_id)

    def cancel_order(self, order_id:UUID) -> Order | None:
        return self.repo.cancel_order(order_id)