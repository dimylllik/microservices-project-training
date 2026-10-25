from order_service import OrderService
from schemas import OrderCreate, OrderItemCreate
import pytest
from models import Order
from uuid import UUID

class FakeOrderRepository:
    def __init__(self, order=None):
        self.order = order

    def create_order(self, order):
        return order

    def get_order(self, order_id):
        return self.order

    def cancel_order(self, order_id):
        self.order.status = "CANCELLED"
        return self.order

    
def test_paid_order_cannot_be_cancelled():
    order = Order(status="PAID")
    repo = FakeOrderRepository(order)
    service = OrderService(repo)

    with pytest.raises(ValueError):
        service.cancel_order(
            UUID("11111111-1111-4111-8111-111111111111")
        )

def test_cancelled_order_is_returned():
    order = Order(status="CANCELLED")
    repo = FakeOrderRepository(order)
    service = OrderService(repo)

    result = service.cancel_order(
        UUID("11111111-1111-4111-8111-111111111111")
    )

    assert result is order

def test_pending_order_is_cancelled():
    order = Order(status="PENDING")
    repo = FakeOrderRepository(order)
    service = OrderService(repo)

    result = service.cancel_order(
        UUID("11111111-1111-4111-8111-111111111111")
    )

    assert result is order
    assert result.status == "CANCELLED"

def test_missing_order_returns_none():
    repo = FakeOrderRepository()
    service = OrderService(repo)

    result = service.cancel_order(
        UUID("11111111-1111-4111-8111-111111111111")
    )

    assert result is None

def test_order_total_is_calculated():
    repo = FakeOrderRepository()
    service = OrderService(repo)

    data = OrderCreate(
        user_id="11111111-1111-4111-8111-111111111111",
        items=[
            OrderItemCreate(
                product_id="22222222-2222-4222-8222-222222222222",
                quantity=2,
                price=100
            ),
            OrderItemCreate(
                product_id="33333333-3333-4333-8333-333333333333",
                quantity=3,
                price=50
            )
        ]
    )

    order = service.create_order(data)

    assert order.total == 350
    assert len(order.items) == 2