from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id_auth0 = Column(String(100), primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)  # Campo opcional

    # Relaciones
    accounts = relationship("Account", back_populates="user")

    def __repr__(self):
        return (
            f"<User(first_name={self.first_name}, "
            f"last_name={self.last_name})>"
        )
