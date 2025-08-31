from PySide6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QFrame,
 	QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from models.game import Game
class UserCard(QFrame):
	def __init__(self):
		super().__init__()
		self.setFrameShape(QFrame.Shape.StyledPanel)
		self.setFrameShadow(QFrame.Shadow.Raised)
		self.setObjectName("user_card")
		self.setMaximumHeight(130)

		self.card_layout = QHBoxLayout(self)
		self.card_layout.setContentsMargins(5, 5, 5, 5)

		profile_pic_container = QWidget()
		profile_pic_layout = QVBoxLayout(profile_pic_container)
		self.profile_pic_label = QLabel()
		
		profile_pic_layout.addWidget(self.profile_pic_label, alignment=Qt.AlignmentFlag.AlignLeft)
		self.card_layout.addWidget(profile_pic_container)

		info_container = QWidget()
		info_layout = QVBoxLayout(info_container)

		self.username_label = QLabel("Username: Loading...")
		self.points_label = QLabel("Total Points: Loading...")
		self.last_activity_label = QLabel("Last Activity: Loading...")
  
		info_layout.addWidget(self.username_label)
		info_layout.addWidget(self.points_label)
		info_layout.addWidget(self.last_activity_label)
		info_layout.addStretch()
  
		self.card_layout.addWidget(info_container)
		self.card_layout.addStretch()

	def update_profile_pic(self, pixmap):
		self.profile_pic_label.setPixmap(pixmap)
  
	def update_user_info(self, user_profile_data):
		"""Updates the view with data from the controller."""
		if user_profile_data:
			self.username_label.setText(f"Username: {user_profile_data.username}")
			self.points_label.setText(f"Total Points: {user_profile_data.total_points}")
			self.last_activity_label.setText("Last Activity: Just now!")

class GameCard(QFrame):
	def __init__(self):
		super().__init__()
		self.setFrameShape(QFrame.Shape.StyledPanel)
		self.setObjectName("game_card")

		self.card_layout = QHBoxLayout(self)
		self.card_layout.setContentsMargins(5, 5, 5, 5)
		self.card_layout.setSpacing(10)

		game_pic_container = QWidget()
		game_pic_layout = QVBoxLayout(game_pic_container)
		self.game_pic_label = QLabel()
		
		pixmap = QPixmap()
		self.game_pic_label.setPixmap(pixmap)
		game_pic_layout.addWidget(self.game_pic_label, alignment=Qt.AlignmentFlag.AlignCenter)
		self.card_layout.addWidget(game_pic_container)

		info_container = QWidget()
		info_layout = QVBoxLayout(info_container)

		self.title_label = QLabel()
		self.achievement_number_label = QLabel()

  
		info_layout.addWidget(self.title_label)
		info_layout.addWidget(self.achievement_number_label)
		info_layout.addStretch() 
  
		self.card_layout.addWidget(info_container)
		self.card_layout.addStretch()

	def update_game_info(self, game_data: Game):
		self.title_label.setText(game_data.title)
		self.achievement_number_label.setText(f"{game_data.num_of_achievements}")
	
	def update_game_pic(self, image_data):
		pixmap = QPixmap()
		if pixmap.loadFromData(image_data):
			self.game_pic_label.setPixmap(pixmap)
		else:
			print("Failed to load image data into QPixmap for game card")
  
  


class RecentlyPlayedFeed(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        self.feed_layout = QVBoxLayout(self)
        self.feed_layout.setContentsMargins(5, 5, 5, 5)
            
    def create_game_card(self):
        game_card = GameCard()
        self.feed_layout.addWidget(game_card)
        return game_card
        
        

		
class UserDashboard(QWidget):
	  
	def __init__(self):
		super().__init__()
		self.setWindowTitle("RetroAchievements Dashboard")
		self.setGeometry(100,100,800,600)
  
		main_layout = QVBoxLayout(self)

		self.user_card = UserCard()
		self.recently_played_games = RecentlyPlayedFeed()
  
		scroll_area = QScrollArea()
		scroll_area.setWidget(self.recently_played_games)
		scroll_area.setWidgetResizable(True)


		main_layout.addWidget(self.user_card)
		main_layout.addWidget(scroll_area)
  
	
