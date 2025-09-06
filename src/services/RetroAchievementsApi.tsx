import {
	AuthObject,
	buildAuthorization,
	getUserCompletionProgress,
	getUserProfile,
	UserCompletionProgress,
	UserProfile,
} from "@retroachievements/api";
import { useEffect, useState } from "react";

export const useRetroAchievements = ({
	username,
	apiKey,
}: {
	username: string;
	apiKey: string;
}) => {
	const [user, setUser] = useState<UserProfile>();
	const [completionProgress, setCompletionProgress] =
		useState<UserCompletionProgress>();
	const [auth, setAuth] = useState<AuthObject>(
		buildAuthorization({
			username,
			webApiKey: apiKey,
		})
	);

	const fetchUserProfile = async () => {
		try {
			const userProfile = await getUserProfile(auth, {
				username,
			});
			setUser(userProfile);
		} catch (err) {
			console.error(err);
		}
	};

	const fetchUserCompletionProgress = async () => {
		try {
			if (user) {
				const completionProgress = await getUserCompletionProgress(auth, {
					username: user.ulid,
					count: 500,
					offset: 0,
				});
				setCompletionProgress(completionProgress);
			}
		} catch (err) {
			console.error(err);
		}
	};

	return {
		user,
		completionProgress,
		fetchUserProfile,
		fetchUserCompletionProgress,
	};
};
