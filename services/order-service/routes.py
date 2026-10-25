from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from order_repository import OrderRepository
from order_service import OrderService
from schemas import OrderCreate, OrderRead
from uuid import UUID

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=201)
def order_create(data:OrderCreate, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = OrderService(repo)
    return service.create_order(data)

@router.get('/user/{user_id}', response_model=list[OrderRead], status_code=200)
def get_orders(user_id : UUID, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = OrderService(repo)
    return service.get_user_orders(user_id)

@router.get('/{order_id}', response_model=OrderRead, status_code=200)
def get_order(order_id: UUID, db:Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = OrderService(repo)
    order = service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@router.post('/{order_id}/cancel', response_model=OrderRead,status_code=200)
def order_cancel(order_id: UUID, db:Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = OrderService(repo)
    try:
        order = service.cancel_order(order_id)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    if order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    return order
