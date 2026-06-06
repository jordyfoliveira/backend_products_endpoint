import { useEffect, useState } from "react";
import { getProducts } from "../services/productService";

type Product = { id: number; display_id: string; sku: string; name: string; description: string; price: number; stock: number; is_active: boolean };

export default function Products() {
    const [products, setProducts] = useState<Product[]>([]);

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "/";
            return;
        }

        async function loadProducts() {
            const data = await getProducts();
            setProducts(data);
        }

        loadProducts();
    }, []);

    return (
    <>
        <h2>Products</h2>

        <div className="logout-container">
            <button className="logout-btn" onClick={logout}>
                Logout
            </button>
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>SKU</th>
                    <th>Nome</th>
                    <th>Preço</th>
                    <th>Stock</th>
                </tr>
            </thead>

            <tbody>
                {products.map((product) => (
                    <tr key={product.id}>
                        <td>{product.display_id}</td>
                        <td>{product.sku}</td>
                        <td>{product.name}</td>
                        <td>{product.price} €</td>
                        <td>{product.stock}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </>
  );
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
}