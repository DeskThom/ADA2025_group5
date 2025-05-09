from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    userId: int
    username: str
    email: str
    password: str
    type: int  # 1 for Doctor, 2 for User (2 is default)

class CtScan(BaseModel):
    id: int
    image: str  # This would be a binary blob in a real system
    createdAt: datetime
    owner: int

class CtScanAnalysis(BaseModel):
    id: int
    createdAt: datetime
    ctScan: List[CtScan]
    score: float
    owner: int

class Report(BaseModel):
    id: int
    createdAt: datetime
    content: str  # HTML content
    owner: int
    ctScanAnalysis: List[CtScanAnalysis]

class Error(BaseModel):
    code: str
    message: str
    
    
# Example usage
user_example = User(
    userId=1,
    username="johndoe",
    email="john@email.com",
    password="securepassword",
    type=1
)

ct_scan_example = CtScan(
    id=1,
    image="binary_blob_here",
    createdAt=datetime.now(),
    owner=1
)

ct_scan_analysis_example = CtScanAnalysis(
    id=1,
    createdAt=datetime.now(),
    ctScan=[ct_scan_example],
    score=95.5,
    owner=1
)

report_example = Report(
    id=1,
    createdAt=datetime.now(),
    content="<h1>Sample HTML Content</h1>",
    owner=1,
    ctScanAnalysis=[ct_scan_analysis_example]
)

error_example = Error(
    code="404",
    message="Not Found"
)

print(user_example)
print(ct_scan_example)
print(ct_scan_analysis_example)
print(report_example)
print(error_example)