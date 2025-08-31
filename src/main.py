import sys
import os 
from pathlib import Path
import requests
from dotenv import load_dotenv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, 
    QFrame, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QPixmap, QFont, QPalette, QColor, QCursor
from PySide6.QtCore import Qt, Signal
from models.game import Game
from models.user import User
from controllers.dashboard_controller import DashboardController
from services.retroachievements_api import RetroAchievementsAPI
from views.user_dashboard.user_dashboard import UserDashboard

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("RA_USERNAME")
API_KEY = os.getenv("RA_API_KEY")


if __name__ == "__main__":
    
    ra_api = RetroAchievementsAPI(API_KEY)
    app = QApplication([])
    
    dashboard_view = UserDashboard()
    dashboard_controller = DashboardController(view=dashboard_view, ra_api=ra_api)
    
	
    dashboard_view.show()
    sys.exit(app.exec())
