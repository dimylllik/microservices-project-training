from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from user_repository import UserRepository
from user_service import UserService
from user_schemas import UserRead, UserCreate, UserLogin, UserUpdate, Token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(prefix="/users", tags=["users"])
bearer = HTTPBearer()


@router.post("/", response_model=UserRead, status_code=201)
def create_user(data:UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.user_create(data)


@router.post('/login', response_model=Token, status_code=200)
def login(data: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    user = service.get_user_by_email(data.email)
    return service.login(data.password, user)

@router.get('/{user_id}', response_model=UserRead, status_code=200)
def get_user(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    user =  service.get_user(user_id)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

@router.patch('/{user_id}', response_model=UserRead, status_code=200)
def update_user(user_id: str, data: UserUpdate, db: Session = Depends(get_db),
                credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    repo = UserRepository(db)
    service = UserService(repo)
    token = credentials.credentials
    current_user = service.get_current_user(token)
    return service.update_user(user_id, current_user, data)

@router.delete('/{user_id}', response_model=bool, status_code=200)
def delete_user(user_id:str, db: Session = Depends(get_db), 
                credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    repo = UserRepository(db)
    service = UserService(repo)
    token = credentials.credentials
    current_user = service.get_current_user(token)
    return service.delete_user(user_id, current_user)

