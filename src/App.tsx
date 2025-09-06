import { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import appLogo from "/favicon.svg";
import PWABadge from "./PWABadge.tsx";
import "./App.css";
import { useRetroAchievements } from "./services/RetroAchievementsApi.tsx";
import { UserCard } from "./components/UserCard.tsx";

function App() {
	const [count, setCount] = useState(0);
	const username = "itsmoogle";
	const apiKey = "7xj359YLXztut2MQzvZS4v49h8qimn9W";
	const api = useRetroAchievements({ username, apiKey });

	// console.log(api.completionProgress);

	return (
		<>
			<div>
				<UserCard user={api.user} />
			</div>
			<h1>retroachivements-gui</h1>
			<div className="card">
				<button onClick={() => api.fetchUserProfile()}>Fetch User Data</button>
				<p>
					Edit <code>src/App.tsx</code> and save to test HMR
				</p>
			</div>
			<p className="read-the-docs">
				Click on the Vite and React logos to learn more
			</p>
			<PWABadge />
		</>
	);
}

export default App;
