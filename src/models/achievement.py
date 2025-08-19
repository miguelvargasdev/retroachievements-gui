from pydantic import BaseModel
from typing import Optional

class Achievement(BaseModel): 
    ID: int
    NumAwarded: int
    NumAwardedHardcore: int
    Title: str
    Description: Optional[str]
    Points: int
    TrueRatio: float
    Author: Optional[str]
    AuthorULID: Optional[str]
    DateModified: Optional[str]
    DateCreated: Optional[str]
    BadgeName: Optional[str]
    DisplayOrder: Optional[int]
    MemAddr: Optional[str]
    type: Optional[str] = None
    DateEarned: Optional[str] = None