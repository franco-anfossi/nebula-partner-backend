from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    tax_id = Column(String(12), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now().astimezone())

    # Relaciones
    accounts = relationship("Account", back_populates="company")
    supplier = relationship("Supplier", uselist=False, back_populates="company")
    # buyer = relationship("Buyer", uselist=False, back_populates="company")

    def __repr__(self):
        return (
            f"<Company(name={self.legal_name}, "
            f"tax_id={self.tax_id}, "
            f"active={self.is_active})>"
        )
