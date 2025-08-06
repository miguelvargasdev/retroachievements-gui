from pydantic import BaseModel
from typing import Optional

class User(BaseModel): 
    ULID: str
    User: str
    UserPic: str
    RichPresenceMsg: str
    TotalPoints: int
    TotalSoftcorePoints: int
    TotalTruePoints: int
    
    
    