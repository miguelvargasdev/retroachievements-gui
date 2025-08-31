import requests
from models.user import User
from models.game import Game

API_BASE = "https://retroachievements.org/API/"

class RetroAchievementsAPI:
	def __init__(self, api_key: str):
		self.api_key = api_key
	
	def get_user_profile(self, username: str):
		url = API_BASE + "API_GetUserProfile" + ".php?"
		params = {
			"y": self.api_key,
			"u": username
		}

		try:
			response = requests.get(url, params)
			response.raise_for_status()
			user_profile = response.json()
   
			return User(user_profile['ULID'], user_profile['User'], user_profile['UserPic'],user_profile['RichPresenceMsg'], user_profile['TotalSoftcorePoints'], user_profile['TotalPoints'])
		except requests.RequestException as e:
			print(f"Error making request: {e}")
			return None

	def get_user_recently_played_games(self, ulid: str):
		url = API_BASE + "API_GetUserRecentlyPlayedGames" + ".php?"
		params = {
			"y": self.api_key,
			"u": ulid,
		}
  
		try:
			response = requests.get(url, params)
			response.raise_for_status()
			recently_played_games = response.json()

			formatted_games = []
			for game in recently_played_games:
				formatted_games.append(Game(game['GameID'],game['Title'], game['ConsoleName'],game['ImageIcon'], game['AchievementsTotal'], {}))
   
			return formatted_games

		except requests.RequestException as e:
			print(f"Error making request: {e}")
			return None

	def get_user_game_progress(self, ulid, game_id):
		url = API_BASE + "API_GetGameInfoAndUserProgress" + ".php?"
		params = {
			"y": self.api_key,
			"u": ulid,
			"g": game_id,
			"a": 1
		}
		try:
			response = requests.get(url, params)
			response.raise_for_status()
			game_progress = response.json()
   
			return game_progress
		except requests.RequestException as e:
			print(f"Error making request: {e}")
			return None

	def get_all_completion_progress(self, ulid):
		all_results = []
		current_offset = 0
		total = 0
		endpoint = "API_GetUserCompletionProgress.php?"
  
		first_page = self._fetch_page(endpoint, ulid, current_offset, 500)
  
		if not first_page:
			return None

		all_results.extend(first_page["Results"])
		current_offset += first_page["Count"]
		total = first_page["Total"]
		
		while current_offset < total:
			next_page = self._fetch_page(endpoint, ulid, current_offset, 500)
			
			if not next_page:
				return None
			all_results.extend(next_page["Results"])
			current_offset += next_page["Count"]

		formatted_games = []
		for game in all_results:
			formatted_games.append(Game(game['GameID'],game['Title'], game['ConsoleName'],game['ImageIcon'], game['NumAwarded'], {}))
  
		return formatted_games

	def _fetch_page(self, endpoint, ulid, offset, count):
		try:
			url = API_BASE + endpoint
			params ={
			"y": self.api_key,
			"u": ulid,
			"c": count,
			"o": offset
			}
			response = requests.get(url, params)
			response.raise_for_status()
			return response.json()
		except requests.RequestException as e:
			print(f"Error making request: {e}")
			raise

   
	def get_image(self, image_path: str):
		url = "https://media.retroachievements.org" + image_path
		try: 
			response = requests.get(url)
			response.raise_for_status()
			return response.content

		except requests.RequestException as e:
			print(f"Error making request: {e}")
			return None