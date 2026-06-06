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

export async function updateStock(productId: number, stock: number) {
    const token = localStorage.getItem("token");
    const response = await api.patch(`/products/${productId}/stock`, { stock }, { headers: { Authorization: `Bearer ${token}` } });
    return response.data;
}

export async function updatePrice(productId: number, price: number) {
    const token = localStorage.getItem("token");
    const response = await api.patch(`/products/${productId}/price`, { price }, { headers: { Authorization: `Bearer ${token}` } });
    return response.data;
}