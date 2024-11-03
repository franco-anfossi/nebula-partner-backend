from sqlalchemy import Column, Integer, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from ...database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(UUID, ForeignKey("user_profiles.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # NULL si es cuenta personal
    is_active = Column(Boolean, default=True)  # Activo/Inactivo

    # Relaciones
    user_profile = relationship("UserProfile", back_populates="accounts")
    company = relationship("Company", back_populates="accounts")

    def __repr__(self):
        return f"<Account(user_profile_id={self.user_profile_id}, company_id={self.company_id}, is_active={self.is_active})>"
