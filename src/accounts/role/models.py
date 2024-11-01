from sqlalchemy import Column, Integer, String
from ...database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # Nombre único del rol
    description = Column(String(255), nullable=True)  # Descripción opcional del rol

    def __repr__(self):
        return f"<Role(name={self.name})>"
