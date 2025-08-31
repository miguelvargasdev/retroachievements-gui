from services.retroachievements_api import RetroAchievementsAPI

MY_API_KEY = "7xj359YLXztut2MQzvZS4v49h8qimn9W"
TEST_USERNAME = "itsmoogle"

def run_test():
	"""
	A simple function to test the RetroAchievements API client.
	"""
  
	api_client = RetroAchievementsAPI(api_key=MY_API_KEY)
	
	user_data = api_client.get_user_profile(username=TEST_USERNAME)
	ulid = user_data.ulid
	recently_played_games = api_client.get_user_recently_played_games(ulid)
	game_progress = api_client.get_user_game_progress(ulid, recently_played_games[0].id)
	all_completion_data = api_client.get_all_completion_progress(ulid)
	if user_data:
		print("Success! User data fetched:")
		print(f"User ID: {user_data.ulid}")
		print(f"Username: {user_data.username}")
		print(f"Profile Pic: {user_data.user_pic_path}")
		print(f"Total Points: {user_data.total_points}")
	else:
		print("Failed to fetch user data.")
		
	if recently_played_games:
		print("Success! Recently played games data fetched:")
		print(f"First Game ID: {recently_played_games[0].id}")
	else:
		print("Failed to fetch recently played games data.")
		
	if game_progress:
		print("Success! Recently played games data fetched:")
		print(f"First Game Title: {game_progress['Title']}")
	else:
		print("Failed to fetch recently played games data.")
		
	if all_completion_data:
		print("Success! Game completion data fetched:")
		print(all_completion_data)

if __name__ == "__main__":
	run_test()
