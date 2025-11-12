from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=True)
    members = relationship("Person", back_populates="household", cascade="all, delete-orphan")

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    married = Column(Boolean, default=False)
    other_info = Column(String, nullable=True)
    household = relationship("Household", back_populates="members")
