from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from ...database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)  # Campo opcional

    # Relaciones
    accounts = relationship("Account", back_populates="user_profile")

    def __repr__(self):
        return f"<UserProfile(first_name={self.first_name}, last_name={self.last_name})>"
