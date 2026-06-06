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

export type ProductCreate = {
    sku: string;
    name: string;
    description: string;
    price: number;
    stock: number;
};

export async function createProduct(product: ProductCreate) {
    const token = localStorage.getItem("token");

    const response = await api.post("/products", product, {
        headers: { Authorization: `Bearer ${token}` }
    });

    return response.data;
}