import { UserProfile } from "@retroachievements/api";
import styles from "./UserCard.module.css";

export const UserCard = ({ user }: { user: UserProfile | undefined }) => {
	const url = "https://media.retroachievements.org/" + user?.userPic;
	return (
		<div className={styles.UserCard}>
			<div>
				<img src={url} />
			</div>
			<div
				style={{
					display: "flex",
					flexDirection: "column",
					justifyContent: "flex-start",
					alignItems: "flex-start",
				}}
			>
				<span className={styles.Username}>{user?.user}</span>
				Total:{" "}
				{user?.totalPoints ? user?.totalPoints : user?.totalSoftcorePoints}
			</div>
			<div>Unfinished Beaten Mastered</div>
		</div>
	);
};
