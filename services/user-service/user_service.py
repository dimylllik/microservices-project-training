from user_repository import UserRepository
from models import User
from user_schemas import UserCreate, UserUpdate
import uuid
from fastapi import HTTPException, status
from security import hash_password
from security import verify_password, create_access_token
import jwt
from security import SECRET_KEY, ALGORITHM
from jwt.exceptions import InvalidTokenError


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def user_create(self, data: UserCreate):
        user = self.repo.exist_email(data.email)
        if user:
            user = User(
                id = uuid.uuid4(),
                name = data.name,
                email = data.email ,
                password_hash=hash_password(data.password)
            )
            return self.repo.create_user(user)
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует"
            ) 

    def get_user(self,user_id:str) -> User | None:
        return self.repo.get_user_by_id(user_id)
    
    def get_user_by_email(self,email:str) -> User | None:
            return self.repo.email_user(email)

    def delete_user(self, user_id: str, current_user: User) -> bool:
        if user_id == str(current_user.id) or current_user.role == "admin":
            return self.repo.delete_user_by_id(user_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Не достаточно прав"
            )

    def update_user(self, user_id: str, current_user: User, data: UserUpdate):
        changes = data.model_dump(exclude_unset=True)
        if not changes:
            raise HTTPException(
                status_code=400,
                detail="Не переданы поля для обновления"
            )
        
        if "name" in changes and changes["name"] is None:
            raise HTTPException(
                status_code=400,
                detail="Имя не может быть null"
            )
        if "email" in changes and changes["email"] is None:
            raise HTTPException(
                status_code=400,
                detail="Email не может быть null"
            )

        user = self.repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
        if user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нельзя изменить данные другого пользователя"
            )
        if "email" in changes:
            owner = self.repo.email_user(changes["email"])

            if owner is not None and owner.id != user.id:
                raise HTTPException(
                    status_code=409,
                    detail="Пользователь с таким email уже существует"
                )
            
        return self.repo.update_user(user_id, changes)


    def login(self, psw: str, user: User):
        if user:
            if verify_password(psw, user.password_hash):
                data={"sub": str(user.id)}
                access_token = create_access_token(data)
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            ) 

    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"require": ["sub", "exp"]},
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Токен недействителен или срок его действия истёк",
            )
        user_id = payload["sub"]
        user = self.repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Не удалось подтвердить пользователя",
            )

        return user
