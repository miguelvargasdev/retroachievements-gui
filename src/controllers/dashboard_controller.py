from PySide6.QtGui import QPixmap
from models.user import User
from models.game import Game
from services.retroachievements_api import RetroAchievementsAPI

class DashboardController:
	def __init__(self, view, ra_api):
		self.view = view
		self.ra_api: RetroAchievementsAPI = ra_api
  
		self.load_user_info("itsmoogle")

	def load_user_info(self, username):
		user_profile: User = self.ra_api.get_user_profile(username)
		
		if user_profile:
			self.view.user_card.update_user_info(user_profile)
			self.load_profile_pic(self.ra_api.get_image(user_profile.user_pic_path))
   
			all_game_data = self.ra_api.get_all_completion_progress(user_profile.ulid)
			self.load_game_feed(user_profile.ulid, all_game_data)

		else: 
			print("Failed to get user profile data.")
   
	def load_game_feed(self, ulid, recent_games_data):

		for game in recent_games_data:
			game_progress = self.ra_api.get_user_game_progress(ulid, game.id)
			game.achievements = game_progress["Achievements"]

			game_card = self.view.recently_played_games.create_game_card()
			game_card.update_game_info(game)
			game_card.update_game_pic(self.ra_api.get_image(game.image_path))
	 
	def load_profile_pic(self, binary):
		pixmap = QPixmap()
		if pixmap.loadFromData(binary):
			scaled_pixmap = pixmap.scaledToWidth(100)
			self.view.user_card.profile_pic_label.setPixmap(scaled_pixmap)
		else:
			print("Failed to load image data into QPixmap.")
   
	
  
	