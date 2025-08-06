from pydantic import BaseModel
from typing import Optional

class Achievement(BaseModel): 
    ID: int
    Title: str
    Description: str
    Points: int
    # Type: str
    BadgeName: str
    DateEarned: Optional[str] = None
    DateEarnedHardcore: Optional[str] = None