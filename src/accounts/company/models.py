from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from ...database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    tax_id = Column(String(12), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)  # Active/Inactive
    created_at = Column(DateTime, default=datetime.utcnow)  # Creation date

    # Relationships
    accounts = relationship("Account", back_populates="company")

    def __repr__(self):
        return f"<Company(legal_name={self.legal_name}, tax_id={self.tax_id}, is_active={self.is_active})>"


class UserCompanyInvitation(Base):
    __tablename__ = "user_company_invitations"

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    invited_at = Column(DateTime, default=datetime.utcnow)
    is_accepted = Column(Boolean, default=False)  # True if the invitation is accepted

    # Relationships
    user_profile = relationship("UserProfile")
    company = relationship("Company")
    role = relationship("Role")

    def __repr__(self):
        return f"<UserCompanyInvitation(user_profile_id={self.user_profile_id}, company_id={self.company_id}, is_accepted={self.is_accepted})>"
