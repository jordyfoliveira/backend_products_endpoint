import { useState } from "react";
import { login } from "../services/authService";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleLogin() {
        try {
            const data = await login(username, password);
            localStorage.setItem("token", data.access_token);
            window.location.href = "/products";
            // console.log(data);
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <>
            <h2>Login</h2>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            <br />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <br />
            <button onClick={handleLogin}>Entrar</button>
        </>
    );
}

