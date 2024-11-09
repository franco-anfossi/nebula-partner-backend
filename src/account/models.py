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
        return (
            f"<Account(uid={self.user_id}, "
            f"cid={self.company_id}, "
            f"act={self.is_active})>"
        )
