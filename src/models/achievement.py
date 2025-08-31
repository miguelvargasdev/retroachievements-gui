from dataclasses import dataclass
from typing import Optional

@dataclass
class Achievement: 
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
    Type: Optional[str] = None
    DateEarned: Optional[str] = None
    
    @property
    def earned(self):
        return True if self.DateEarned != None else False