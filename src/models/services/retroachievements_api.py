import requests


API_BASE = "https://retroachievements.org/API/"

class RetroAchievementsAPI:
	def __init__(self, api_key):
		self.api_key = api_key
	
	def get_user_profile(self, username):
		url = API_BASE + "API_GetUserProfile" + ".php?"
		params = {
			"y": self.api_key,
			"u": username
		}

		try:
			response = requests.get(url, params)
			response.raise_for_status()
			user_profile = response.json()
   
			return user_profile
		except requests.RequestException as e:
			print(f"Error making request: {e}")
			return None

	def get_user_recently_played_games(self, ulid):
		url = API_BASE + "API_GetUserRecentlyPlayedGames" + ".php?"
		params = {
			"y": self.api_key,
			"u": ulid,
		}
  
		try:
			response = requests.get(url, params)
			response.raise_for_status()
			recently_played_games = response.json()
   
			return recently_played_games
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