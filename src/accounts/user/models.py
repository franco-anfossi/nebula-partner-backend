from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ...database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String, unique=True, nullable=False)  # Auth0 ID
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)  # Optional phone field
    is_active = Column(Boolean, default=True)  # Active/Inactive
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation date

    # Relationships
    accounts = relationship("Account", back_populates="user_profile")

    def __repr__(self):
        return f"<UserProfile(auth_id={self.auth_id}, first_name={self.first_name}, last_name={self.last_name}, is_active={self.is_active})>"
