from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    userId: Optional[int]
    username: str
    email: str
    type: int = 2
    password: str
    iban: str


class Session(BaseModel):
    sessionId: str
    userId: int
    expiryTime: datetime


class Report(BaseModel):
    id: Optional[int]
    createdAt: datetime
    content: str
    owner: int
    ctScanAnalysis: List["CtScanAnalysis"]


class CtScan(BaseModel):
    id: Optional[int]
    image: str
    createdAt: datetime
    owner: int


class CtScanAnalysis(BaseModel):
    id: Optional[int]
    createdAt: datetime
    ctScan: List[CtScan]
    score: float
    owner: int

class Payment(BaseModel):
    id: Optional[int]
    createdAt: datetime
    amount: float
    userId: int

class Error(BaseModel):
    pass