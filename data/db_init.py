from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid
from datetime import datetime

Base = declarative_base()

# Define User table
class User(Base):
    __tablename__ = 'User'
    userId = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    type = Column(Integer)
    password = Column(String)

    sessions = relationship("Session", back_populates="user")
    reports = relationship("Report", back_populates="owner")
    ct_scans = relationship("CtScan", back_populates="owner")
    ct_scan_analyses = relationship("CtScanAnalysis", back_populates="owner")

# Define Session table
class Session(Base):
    __tablename__ = 'Session'
    sessionId = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    userId = Column(Integer, ForeignKey('User.userId'))
    expiryTime = Column(DateTime)

    user = relationship("User", back_populates="sessions")

# Define Report table
class Report(Base):
    __tablename__ = 'Report'
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    owner = Column(Integer, ForeignKey('User.userId'))

    owner_user = relationship("User", back_populates="reports")

# Define CtScan table
class CtScan(Base):
    __tablename__ = 'CtScan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(LargeBinary)
    createdAt = Column(DateTime, default=datetime.utcnow)
    owner = Column(Integer, ForeignKey('User.userId'))

    owner_user = relationship("User", back_populates="ct_scans")
    ct_scan_analyses = relationship("CtScanAnalysis", secondary="CtScanAnalysisCtScan", back_populates="ct_scans")

# Define CtScanAnalysis table
class CtScanAnalysis(Base):
    __tablename__ = 'CtScanAnalysis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    score = Column(Float)
    owner = Column(Integer, ForeignKey('User.userId'))

    owner_user = relationship("User", back_populates="ct_scan_analyses")
    ct_scans = relationship("CtScan", secondary="CtScanAnalysisCtScan", back_populates="ct_scan_analyses")

# Junction table for CtScan and CtScanAnalysis
class CtScanAnalysisCtScan(Base):
    __tablename__ = 'CtScanAnalysisCtScan'
    ctScanId = Column(Integer, ForeignKey('CtScan.id'), primary_key=True)
    ctScanAnalysisId = Column(Integer, ForeignKey('CtScanAnalysis.id'), primary_key=True)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///aidence.db')

# Create all tables in the database
Base.metadata.create_all(engine)

print("Database schema created successfully.")
