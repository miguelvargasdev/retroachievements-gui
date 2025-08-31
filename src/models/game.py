from dataclasses import dataclass
from typing import Dict, Optional
from models.achievement import Achievement


@dataclass
class Game: 
    id: int
    title: str
    console: str
    image_path: Optional[str]
    num_of_achievements: int
    achievements: Dict[str, Achievement]
    