from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    description = Column(String, nullable=True)  # Descripción de servicios o productos
    keywords = Column(String(255), nullable=True)  # Para busqueda
    category = Column(String(50), nullable=True)  # Categoría del producto o servicio

    # Relación con Company
    company = relationship("Company", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(company_id={self.company_id}, " f"category={self.category})>"
