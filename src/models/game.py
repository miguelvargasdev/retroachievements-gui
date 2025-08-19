from pydantic import BaseModel
from typing import Dict, Optional
from models.achievement import Achievement

class Game(BaseModel): 
    ID: int
    Title: str
    ConsoleName: str
    ImageIcon: Optional[str]
    NumAchievements: int
    Achievements: Dict[str, Achievement]
    