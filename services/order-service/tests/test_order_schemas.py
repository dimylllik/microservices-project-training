import pytest
from pydantic import ValidationError
from schemas import OrderItemCreate, OrderCreate

def test_negative_quantity_is_rejected():
    with pytest.raises(ValidationError):
        OrderItemCreate(
            product_id="22222222-2222-4222-8222-222222222222",
            quantity=-2,
            price=100
        )

def test_negative_price_is_rejected():
    with pytest.raises(ValidationError):
        OrderItemCreate(
            product_id="22222222-2222-4222-8222-222222222222",
            quantity=2,
            price=-100
        )

def test_empty_order_is_rejected():
    with pytest.raises(ValidationError):
        OrderCreate(
            user_id="11111111-1111-4111-8111-111111111111",
            items=[]
        )

def test_valid_order_item_is_created():
    item = OrderItemCreate(
        product_id="22222222-2222-4222-8222-222222222222",
        quantity=2,
        price=100
    )

    assert item.quantity == 2
    assert item.price == 100 

def test_zero_quantity_is_rejected():
    with pytest.raises(ValidationError):
        OrderItemCreate(
            product_id="22222222-2222-4222-8222-222222222222",
            quantity=0,
            price=100            
        )

def test_zero_price_is_allowed():
    OrderItemCreate(
            product_id="22222222-2222-4222-8222-222222222222",
            quantity=1,
            price=0    
    )
