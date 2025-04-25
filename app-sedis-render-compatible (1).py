# PIM Simple (inspiré d'Akeneo) - Version UX/UI améliorée pour SEDIS

from flask import Flask, jsonify, request, render_template_string
from uuid import uuid4
import os

app = Flask(__name__)

# In-memory database
products = {}
categories = {}

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(list(products.values())), 200

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product_id = str(uuid4())
    product = {
        'id': product_id,
        'name': data.get('name'),
        'description': data.get('description', ''),
        'category_id': data.get('category_id'),
        'attributes': data.get('attributes', {})
    }
    products[product_id] = product
    return jsonify(product), 201

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200

@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.json
    category_id = str(uuid4())
    category = {
        'id': category_id,
        'name': data.get('name')
    }
    categories[category_id] = category
    return jsonify(category), 201

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product), 200

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>PIM SEDIS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #f5f5f5;
        }
        header {
            background-color: #ba0c2f;
            color: white;
            padding: 1em;
            text-align: center;
        }
        .container {
            margin: 2em auto;
            padding: 2em;
            background: white;
            max-width: 900px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        form input, form textarea {
            width: 100%;
            margin-bottom: 1em;
            padding: 0.8em;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        form button {
            background-color: #ba0c2f;
            color: white;
            padding: 0.8em 2em;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background: #e0e0e0;
            margin-bottom: 1em;
            padding: 1em;
            border-radius: 5px;
        }
        footer {
            margin-top: 2em;
            text-align: center;
            font-size: 0.8em;
            color: #888;
        }
    </style>
</head>
<body>
<header>
    <h1>PIM SEDIS - Gestion de Produits</h1>
</header>
<div class='container'>
    <form id='productForm'>
        <h2>Ajouter un produit</h2>
        <input type='text' name='name' placeholder='Nom du produit' required>
        <input type='text' name='description' placeholder='Description'>
        <input type='text' name='category_id' placeholder='ID Catégorie'>
        <textarea name='attributes' placeholder='Attributs (JSON)'></textarea>
        <button type='submit'>Créer</button>
    </form>

    <h2>Liste des produits</h2>
    <ul id='productList'></ul>
</div>
<footer>
    &copy; 2025 SEDIS - Tous droits réservés.
</footer>

<script>
document.getElementById("productForm").onsubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
        name: form.name.value,
        description: form.description.value,
        category_id: form.category_id.value,
        attributes: JSON.parse(form.attributes.value || '{}')
    };
    await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    form.reset();
    loadProducts();
};

async function loadProducts() {
    const res = await fetch('/api/products');
    const products = await res.json();
    const list = document.getElementById("productList");
    list.innerHTML = '';
    products.forEach(p => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${p.name}</strong> <br> ${p.description} <br><small>Catégorie: ${p.category_id}</small>`;
        list.appendChild(li);
    });
}

loadProducts();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
