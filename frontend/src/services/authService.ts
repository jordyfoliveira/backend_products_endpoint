import api from "../api/api";

export async function login(username: string, password: string) {
    const response = await api.post("/auth/login", { username, password });
    
    return response.data;
}
