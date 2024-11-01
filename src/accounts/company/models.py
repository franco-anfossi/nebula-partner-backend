from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ...database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String(255), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    estado = Column(Boolean, default=True)  # Activo/Inactivo
    creado_en = Column(DateTime, default=datetime.utcnow)  # Fecha de creación

    def __repr__(self):
        return f"<Empresa(razon_social={self.razon_social}, rut={self.rut}, estado={self.estado})>"
