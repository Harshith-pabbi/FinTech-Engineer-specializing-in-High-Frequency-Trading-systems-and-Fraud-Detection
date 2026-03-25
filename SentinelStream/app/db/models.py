from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class DimUser(Base):
    __tablename__ = "dim_users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    transactions = relationship("FactTransaction", back_populates="user")

class DimMerchant(Base):
    __tablename__ = "dim_merchants"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String, index=True)
    location = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    transactions = relationship("FactTransaction", back_populates="merchant")

class FactTransaction(Base):
    __tablename__ = "fact_transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("dim_users.id"), index=True)
    merchant_id = Column(String, ForeignKey("dim_merchants.id"), index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")
    risk_score = Column(Float, nullable=True)
    is_fraudulent = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    user = relationship("DimUser", back_populates="transactions")
    merchant = relationship("DimMerchant", back_populates="transactions")
