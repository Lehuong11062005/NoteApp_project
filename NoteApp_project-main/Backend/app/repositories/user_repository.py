from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user_data, hashed_password):
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user