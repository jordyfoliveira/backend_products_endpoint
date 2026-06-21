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
    const [search, setSearch] = useState("");
    const [sortField, setSortField] = useState<keyof Product>("name");
    const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

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

    function handleSearch(products: Product[], search: string): Product[] {
    const value = search.toLowerCase();

    return products.filter((product) => product.sku?.toLowerCase().includes(value) || product.name?.toLowerCase().includes(value) || product.display_id?.toLowerCase().includes(value)
        );
    }

    function handleSortProducts(products: Product[]): Product[] {
    return [...products].sort((a, b) => {
        let result = 0;

        if (sortField === "display_id") result = a.display_id.localeCompare(b.display_id);
        if (sortField === "sku") result = a.sku.localeCompare(b.sku);
        if (sortField === "name") result = a.name.localeCompare(b.name);
        if (sortField === "price") result = a.price - b.price;
        if (sortField === "stock") result = a.stock - b.stock;

        return sortDirection === "asc" ? result : -result;}
        );
    }

    function handleSort(field: keyof Product) {
    if (sortField === field) setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    else {
        setSortField(field);
        setSortDirection("asc");
        }
    }

    const filteredProducts = handleSearch(products, search);
    const sortedProducts = handleSortProducts(filteredProducts);

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

        <input
            className="search-box"
            type="text"
            placeholder="Pesquisar por SKU ou Nome..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
        />

        <table>
            <thead>
                <tr>
                    <th onClick={() => handleSort("sku")}>SKU {sortField === "sku" ? (sortDirection === "asc" ? "▲" : "▼") : ""}</th>
                    <th onClick={() => handleSort("name")}>Nome {sortField === "name" ? (sortDirection === "asc" ? "▲" : "▼") : ""}</th>
                    <th onClick={() => handleSort("price")}>Preço {sortField === "price" ? (sortDirection === "asc" ? "▲" : "▼") : ""}</th>
                    <th onClick={() => handleSort("stock")}>Stock {sortField === "stock" ? (sortDirection === "asc" ? "▲" : "▼") : ""}</th>
                    <th>Ações</th>
                </tr>
            </thead>

            <tbody>
                {sortedProducts.map((product) => (
                    <tr key={product.id}>
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