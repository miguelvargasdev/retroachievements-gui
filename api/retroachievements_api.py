import requests
import os
import pickle
import time
from typing import List
from models.user import User
from models.game import Game

API_BASE = "https://retroachievements.org/API/"
API_KEY = ""

CACHE_FILE = "ra_cache.pkl"
CACHE_TTL = 1800
ICON_CACHE_DIR = "cache/icons"
os.makedirs(ICON_CACHE_DIR, exist_ok=True)

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        cache_data = pickle.load(f)
else:
	cache_data = {
		"user_profile": {},
		"recent_games": {},
		"game_info": {},

	}

def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache_data, f)

def is_cache_valid(entry):
    return(time.time() - entry["timestamp"]) < CACHE_TTL

def get_user_profile(username: str) -> User:
    """    Fetch user profile by username.    """
    if username in cache_data["user_profile"]:
        entry = cache_data["user_profile"][username]
        if is_cache_valid(entry):
            return User.model_validate(entry["data"])
    
    url = f"{API_BASE}API_GetUserProfile.php"
    params = {"u": username, "y": API_KEY}
    print("Running GET USER PROFILE REQEUST")
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    user = User(**response.json())
    cache_data["user_profile"][username] = {"data": user.model_dump(), "timestamp": time.time()}
    save_cache()
    return user

def get_user_recently_played_games(ulid: str) -> List[Game]:
	"""Fetch recently played games for a user by ULID. Returns lightweight Game objects without achievements."""
	if ulid in cache_data["recent_games"]:
		entry = cache_data["recent_games"][ulid]
		if is_cache_valid(entry):
			return [Game.model_validate(g) for g in entry["data"]]

	url = f"{API_BASE}API_GetUserRecentlyPlayedGames.php"
	params = {"u": ulid, "y": API_KEY}
	print("Running GET USER RECENTLY PLAYED GAMES REQEUST")

	response = requests.get(url, params=params)
	response.raise_for_status()
 
	games_raw = response.json()
	games = []
	for g in games_raw:
		game = Game(
			ID=g["GameID"],
			Title=g.get("Title", "Unknown"),
			ConsoleName=g.get("ConsoleName", ""),
			ImageIcon=g.get("ImageIcon", ""),
			NumAchievements=g.get("NumAchievements", 0),
			Achievements={}, 
		)
		games.append(game)
	cache_data["recent_games"][ulid] = {"data": [game.model_dump() for game in games], "timestamp": time.time()}
	save_cache()
	return games


def get_game_info_and_user_progress(ulid:str, game_id: int) -> Game:
	"""Fetch detailed game info and user's achievement progress."""
	cache_key = (ulid, game_id)
	if cache_key in cache_data["game_info"]:
		entry = cache_data["game_info"][cache_key]

		if is_cache_valid(entry):
			return Game.model_validate(entry["data"])


	url = f"{API_BASE}API_GetGameInfoAndUserProgress.php"
	params = {"u": ulid, "y": API_KEY, "g": game_id}
	print("Running GET GAME INFO AND USER PROGRESS")

	response = requests.get(url, params=params)
	response.raise_for_status()
 
	game = Game(**response.json())
	cache_data["game_info"][cache_key] = {"data": game.model_dump(), "timestamp": time.time()}
	save_cache()
	return game

def get_achievement_icon(badge_name: str) -> str:
    icon_path = os.path.join(ICON_CACHE_DIR, f"{badge_name}.png")
    
    if not os.path.exists(icon_path):
        url= f"https://retroachievements.org/Badge/{badge_name}.png"
        try: 
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(icon_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download icon {badge_name}: {e}")
            return None
        
    return icon_path