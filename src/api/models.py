from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    avatar: Mapped[str] = mapped_column(String(
        120), nullable=False, default="https://randomuser.me/api/portraits/men/4.jpg")
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    salt: Mapped[str] = mapped_column(String(80), nullable=False, default=1)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "lastname": self.lastname,
            "avatar": self.avatar
            # do not serialize the password, its a security breach
        }
