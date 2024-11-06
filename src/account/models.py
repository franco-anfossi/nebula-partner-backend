from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id_auth0"), nullable=False)
    company_id = Column(
        Integer, ForeignKey("companies.id"), nullable=True
    )  # NULL si es cuenta personal
    is_active = Column(Boolean, default=True)  # Activo/Inactivo

    # Relaciones
    user = relationship("User", back_populates="accounts")
    company = relationship("Company", back_populates="accounts")

    def __repr__(self):
        return f"<Account(user_id={self.user_id}, company_id={self.company_id}, is_active={self.is_active})>"
