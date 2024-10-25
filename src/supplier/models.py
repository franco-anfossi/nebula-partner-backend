from sqlalchemy import Column, Integer, String

from ..database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String, unique=True, nullable=False)  # ID de Auth0
    description = Column(String, nullable=True)  # Descripción opcional del proveedor

    def __repr__(self):
        return f"<Supplier(auth_id={self.auth_id}, description={self.description})>"
