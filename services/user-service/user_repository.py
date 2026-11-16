from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_role_user_by_id(self, user_id: str):
        ur = self.db.query(User).filter(User.id == user_id).first()
        if ur:
            return ur.role

    def delete_user_by_id(self, user_id: str) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        else:
            return False

    def exist_email(self, email: str) -> bool:
        ur = self.db.query(User).filter(User.email == email).first()
        if ur:
            return False
        else:
            return True

    def email_user(self, email: str) -> User | None:
        ur = self.db.query(User).filter(User.email == email).first()
        if ur:
            return ur
        else: 
            return None

    def update_user(self, user_id: str, changes: dict) -> User | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            if "name" in changes:
                user.name = changes['name']
            if "email" in changes:
                user.email = changes['email']
            self.db.commit()
            self.db.refresh(user)
            return user
        else:
            return None