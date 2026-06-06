import api from "../api/api";

export async function getProducts() {
    const token = localStorage.getItem("token");

    const response = await api.get("/products", {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    return response.data;
}