from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ...database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # Null if it's a personal account
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    user_profile = relationship("UserProfile", back_populates="accounts")
    company = relationship("Company", back_populates="accounts")
    roles = relationship("AccountRole", back_populates="account")

    def __repr__(self):
        return f"<Account(user_profile_id={self.user_profile_id}, company_id={self.company_id}, is_active={self.is_active})>"
    

class AccountRole(Base):
    __tablename__ = "account_roles"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # Relationships
    account = relationship("Account", back_populates="roles")
    role = relationship("Role")

    def __repr__(self):
        return f"<AccountRole(account_id={self.account_id}, role_id={self.role_id})>"
