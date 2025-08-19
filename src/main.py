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

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("RA_USERNAME")
API_KEY = os.getenv("RA_API_KEY")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.exit(app.exec())
