import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, 
    QFrame, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QPixmap, QFont, QPalette, QColor, QCursor
from PySide6.QtCore import Qt, Signal
from models.game import Game
from models.user import User
from api.retroachievements_api import get_game_info_and_user_progress, get_user_profile, get_user_recently_played_games, get_achievement_icon

USERNAME = ""

class ClickableGameCard(QFrame):
    clicked = Signal(int)  # will emit game ID

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QHBoxLayout(self)

        # Game Image
        self.image_label = QLabel()
        if self.game.ImageIcon:
            try:
                image_response = requests.get(f"https://retroachievements.org{self.game.ImageIcon}")
                pixmap = QPixmap()
                pixmap.loadFromData(image_response.content)
                self.image_label.setPixmap(pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            except:
                self.image_label.setText("No image")
        layout.addWidget(self.image_label, stretch=0)

        # Text info container
        text_container = QVBoxLayout()
        title_label = QLabel(f"{self.game.Title} | ID: {self.game.ID}")
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPixelSize(14)
        title_label.setFont(title_font)

        platform_label = QLabel(self.game.ConsoleName)
        platform_palette = platform_label.palette()
        platform_palette.setColor(QPalette.WindowText, QColor('gray'))
        platform_font = platform_label.font()
        platform_font.setPixelSize(12)
        platform_label.setFont(platform_font)
        platform_label.setPalette(platform_palette)

        text_container.addWidget(title_label)
        text_container.addWidget(platform_label)
        text_container.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        layout.addLayout(text_container, stretch=1)

    def mousePressEvent(self, event):
        self.clicked.emit(self.game.ID)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RetroAchievements Client")
        self.setGeometry(200, 200, 600, 600)
        
        container = QWidget()
        layout = QVBoxLayout(container)
    
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

        self.cards = {}  # map game ID to card widget (for toggling achievements)
        self.achievements_widgets = {}  # to track achievement displays

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
        card = ClickableGameCard(game)
        card.clicked.connect(self.on_game_card_clicked)
        self.games_layout.addWidget(card)
        self.cards[game.ID] = card

    def on_game_card_clicked(self, game_id: int):
        # Toggle achievements display or load and show if not loaded
        if game_id in self.achievements_widgets:
            widget = self.achievements_widgets[game_id]
            widget.setVisible(not widget.isVisible())
            return

        # Fetch detailed info
        try:
            detailed_game = get_game_info_and_user_progress(USERNAME, game_id)
            achievements = detailed_game.Achievements  # should be a dict

            achievements_container = QWidget()
            achievements_layout = QVBoxLayout()
            achievements_container.setLayout(achievements_layout)

            for ach_id, achievement in achievements.items():
                if achievement.DateEarned:
                    ach_layout = QHBoxLayout()
                    ach_image_label = QLabel()
                    if achievement.BadgeName:
                        icon = get_achievement_icon(achievement.BadgeName)
                        if icon:
                            pixmap = QPixmap(icon)
                            ach_image_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        else:
                            ach_image_label.setText("No Image")
                    ach_layout.addWidget(ach_image_label)

                    ach_title_label = QLabel(f"{achievement.Title} - Points: {achievement.Points}")
                    ach_layout.addWidget(ach_title_label)
                    achievements_layout.addLayout(ach_layout)

            # Insert achievements widget **after** the card in the layout
            card = self.cards[game_id]
            idx = self.games_layout.indexOf(card)
            self.games_layout.insertWidget(idx + 1, achievements_container)
            self.achievements_widgets[game_id] = achievements_container

        except Exception as e:
            self.profile_label.setText(f"Error loading achievements: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
