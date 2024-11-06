from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    tax_id = Column(String(12), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)  # Activo/Inactivo
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación

    # Relaciones
    accounts = relationship("Account", back_populates="company")
    supplier = relationship("Supplier", uselist=False, back_populates="company")
    buyer = relationship("Buyer", uselist=False, back_populates="company")

    def __repr__(self):
        return f"<Company(legal_name={self.legal_name}, tax_id={self.tax_id}, is_active={self.is_active})>"
