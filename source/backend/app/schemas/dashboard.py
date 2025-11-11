from pydantic import BaseModel
from typing import List

class ErrorStat(BaseModel):
    error_type: str
    count: int

class UserDashboardStats(BaseModel):
    total_submissions: int
    common_errors: List[ErrorStat]