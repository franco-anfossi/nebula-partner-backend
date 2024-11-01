from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ...database import Base

class UsuarioPerfil(Base):
    __tablename__ = "usuario_perfiles"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String, unique=True, nullable=False)  # ID de Auth0
    nombre = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefono = Column(String, nullable=True)  # Campo opcional para el teléfono
    estado = Column(Boolean, default=True)  # Activo/Inactivo
    creado_en = Column(DateTime, default=datetime.utcnow)  # Fecha de creación

    # Relación con la tabla intermedia UsuarioEmpresaRol
    empresas_roles = relationship("UsuarioEmpresaRol", back_populates="usuario")

    def __repr__(self):
        return f"<UsuarioPerfil(auth_id={self.auth_id}, nombre={self.nombre}, apellidos={self.apellidos}, estado={self.estado})>"
