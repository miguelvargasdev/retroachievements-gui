from pydantic import BaseModel
from typing import Dict
from models.achievement import Achievement

class Game(BaseModel): 
    ID: int
    Title: str
    ConsoleName: str
    ImageIcon: str
    ImageTitle: str
    ImageIngame: str
    ImageBoxArt: str
    NumAchievements: int
    Achievements: Dict[str, Achievement]
    