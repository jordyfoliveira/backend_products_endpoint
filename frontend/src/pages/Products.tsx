import { useEffect, useState } from "react";
import { getProducts, createProduct, updateStock, updatePrice } from "../services/productService";

type Product = { id: number; display_id: string; sku: string; name: string; description: string; price: number; stock: number; is_active: boolean };

export default function Products() {
    const [products, setProducts] = useState<Product[]>([]);
    const [showForm, setShowForm] = useState(false);
    const [sku, setSku] = useState("");
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("");
    const [stock, setStock] = useState("");

    async function loadProducts() {
        const data = await getProducts();
        setProducts(data);
    }

    async function logout() {
        localStorage.removeItem("token");
        window.location.href = "/";
    }

    async function handleCreateProduct() {
        await createProduct({sku, name, description, price: Number(price), stock: Number(stock)});

        setSku("");
        setName("");
        setDescription("");
        setPrice("");
        setStock("");
        setShowForm(false);
        await loadProducts();
    }

    async function handleUpdatePrice(productId: number) {
        const value = prompt("Novo preço:");

        if (value === null || value.trim() === "") return;

        const price = Number(value);

        if (Number.isNaN(price) || price <= 0) {
            alert("Preço inválido");
            return;
        }

        await updatePrice(productId, price);
        await loadProducts();
    }

    async function handleUpdateStock(productId: number) {
        const value = prompt("Novo stock:");

        if (value === null || value.trim() === "") return;

        const stock = Number(value);

        if (Number.isNaN(stock) || stock < 0) {
            alert("Stock inválido");
            return;
        }

        await updateStock(productId, stock);
        await loadProducts();
    }

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (!token) {
            window.location.href = "/";
            return;
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

        <div className="product-form">
            <button className="new-product-btn" onClick={() => setShowForm(!showForm)}>
                Novo Produto
            </button>

            {showForm && (
                <>
                    <div className="form-row">
                        <input placeholder="SKU" value={sku} onChange={(e) => setSku(e.target.value)} />
                        <input placeholder="Nome" value={name} onChange={(e) => setName(e.target.value)} />
                        <input placeholder="Descrição" value={description} onChange={(e) => setDescription(e.target.value)} />
                        <input placeholder="Preço" value={price} onChange={(e) => setPrice(e.target.value)} />
                        <input placeholder="Stock" value={stock} onChange={(e) => setStock(e.target.value)} />
                    </div>

                    <button className="save-product-btn" onClick={handleCreateProduct}>
                        Guardar
                    </button>
                </>
            )}
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>SKU</th>
                    <th>Nome</th>
                    <th>Preço</th>
                    <th>Stock</th>
                    <th>Ações</th>
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
                        <td>
                            <button onClick={() => handleUpdateStock(product.id)}>Stock</button>
                            <button onClick={() => handleUpdatePrice(product.id)}>Preço</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </>
  );
}