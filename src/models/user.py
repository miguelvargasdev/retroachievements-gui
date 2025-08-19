from dataclasses import dataclass

@dataclass
class User:
	ulid: str
	username: str
	user_pic_path: str
	rich_presence_msg: str
	softcore_points: int
	hardcore_points: int
	
	@property
	def total_points(self):
		return self.hardcore_points if self.hardcore_points > 0 else self.softcore_points

