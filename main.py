import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QFrame, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont, QPalette, QColor
from PySide6.QtCore import Qt
from models.game import Game
from models.user import User

# === RetroAchievements API Config ===

API_BASE = "https://retroachievements.org/API/"
USERNAME = "itsmoogle"
API_KEY = "7xj359YLXztut2MQzvZS4v49h8qimn9W"

# === API Functions ===

def get_user_profile(username: str):
    """Fetch user profile."""
    url = f"{API_BASE}API_GetUserProfile.php"
    params = {
		"u": username,
  		"y": API_KEY,
	}
    response = requests.get(url,params=params)

    response.raise_for_status()
    user = User(**response.json())
    return user

def get_user_recently_played_games(ULID: str):
    """Fetch user recently played games."""
    url = f"{API_BASE}API_GetUserRecentlyPlayedGames.php"
    params = {
		"u": ULID,
		"y": API_KEY,
	}
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    recent_games = response.json()
    games = []
    for game_data in recent_games: 
        game_data = get_game_info_and_user_progress(ULID, game_data.get("GameID", ""))
        game = Game(**game_data)
        games.append(game)
    
    return games

def get_game_info_and_user_progress(ULID: str, game_id: int):
    """Fetches game info and the user's progress for that game."""
    url = f"{API_BASE}API_GetGameInfoAndUserProgress.php"
    params = {
        "u": ULID,
        "y": API_KEY,
        "g": game_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    
    return response.json()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RetroAchievements Client")
        self.setGeometry(200, 200, 600, 400)
        
        container = QWidget()
        layout = QVBoxLayout()
	
        self.profile_label = QLabel("Loading profile...")
        self.profile_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.profile_label)
    
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.games_container = QWidget()
        self.games_layout = QVBoxLayout()
        self.games_container.setLayout(self.games_layout)
        self.scroll_area.setWidget(self.games_container)
        layout.addWidget(self.scroll_area)
        
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.load_user_data()
        
    def load_user_data(self):
        try:
            user = get_user_profile(USERNAME)
            
            score = user.TotalSoftcorePoints
            self.profile_label.setText(f"User: {USERNAME} | Gamerscore: {score}")
            
            recent_games = get_user_recently_played_games(user.ULID)
            for game in recent_games: 
                self.add_game_card(game)
                
        except Exception as e:
            self.profile_label.setText(f"Error loading profile: {e}")
    def add_game_card(self, game: Game):
        """Create a game card with image, title, and system"""
        title = game.Title
        id = game.ID
        console_name = game.ConsoleName
        image_icon = game.ImageIcon
        num_achievements = game.NumAchievements
        
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setLineWidth(1)
   
        card_layout = QHBoxLayout()
        
        image_label = QLabel()
        if image_icon:
            try: 
                image_response = requests.get(f"https://retroachievements.org{image_icon}")
                pixmap = QPixmap()
                pixmap.loadFromData(image_response.content)
                image_label.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except: 
                image_label.setText("No image")
                
        card_layout.addWidget(image_label, stretch=0)
        
        text_container = QVBoxLayout()
        title_label = QLabel(f"{title} | ID: {id} | Achievements: {num_achievements}")
        
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPixelSize(14)
        
        title_label.setFont(title_font)

        platform_label = QLabel(console_name)
        
        platform_palette = platform_label.palette()
        platform_palette.setColor(QPalette.WindowText, QColor('gray'))
        
        platform_font = platform_label.font()
        platform_font.setPixelSize(12)
        
        platform_label.setFont(platform_font)
        platform_label.setPalette(platform_palette)
        
        text_container.addWidget(title_label)
        text_container.addWidget(platform_label)
        # ach_layout = QVBoxLayout()

        # for ach_id, achievement in game.Achievements.items():
        #     if achievement.DateEarned:
                
        #         ach_image_label = QLabel()
        #         ach_image_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         if achievement.BadgeName:
        #             try: 
        #                 image_response = requests.get(f"https://retroachievements.org/Badge/{achievement.BadgeName}.png")
        #                 pixmap = QPixmap()
        #                 pixmap.loadFromData(image_response.content)
        #                 ach_image_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #             except: 
        #                 ach_image_label.setText("No image")        
        #         ach_title_label = QLabel(f"{achievement.Title} - Points: {achievement.Points}")
        #         ach_title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         ach_layout.addWidget(ach_image_label)
        #         ach_layout.addWidget(ach_title_label)
                
                

        
        card_layout.addLayout(text_container, stretch=1)
        # card_layout.addLayout(ach_layout)
        
        card.setLayout(card_layout)
        self.games_layout.addWidget(card)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())