// static/app.js


// Show selected section and hide others
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none'
    })
    document.getElementById(sectionId).style.display = 'block'
    if (sectionId === 'view-inventory') loadInventory()
}


// Load view inventory on page load
document.addEventListener('DOMContentLoaded', () => {
    showSection('view-inventory')
})


// Load all inventory items
function loadInventory() {
    fetch('/inventory')
        .then(res => res.json())
        .then(data => renderTable(data, 'inventory-list'))
}


// Search inventory
function searchInventory() {
    const query = document.getElementById('search-input').value
    fetch(`/inventory/search?q=${query}`)
        .then(res => res.json())
        .then(data => renderTable(data, 'search-results'))
}


// Render inventory items into a table body
function renderTable(items, tbodyId) {
    const tbody = document.getElementById(tbodyId)
    tbody.innerHTML = ''
    items.forEach(item => {
        const row = document.createElement('tr')
        row.innerHTML = `
            <td>${item.id}</td>
            <td><a href="#" onclick="event.preventDefault(); showDetail(${item.id})">${item.product_name}</a></td>
            <td>${item.brands}</td>
            <td>${item.price}</td>
            <td>${item.stock}</td>
            <td>
                <button onclick="editItem(${item.id})">✏️</button>
                <button onclick="deleteItem(${item.id})">🗑️</button>
            </td>
        `
        tbody.appendChild(row)
    })
}


// Add new inventory item
function addItem() {
    const item = {
        product_name: document.getElementById('add-name').value,
        brands: document.getElementById('add-brand').value,
        barcode: document.getElementById('add-barcode').value,
        categories: document.getElementById('add-categories').value,
        ingredients_text: document.getElementById('add-ingredients').value,
        nutrition_grades: document.getElementById('add-grades').value,
        price: parseFloat(document.getElementById('add-price').value),
        stock: parseInt(document.getElementById('add-stock').value)
    }
    fetch('/inventory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('add-message').textContent = data.error
        } else {
            document.getElementById('add-message').textContent = `${data.product_name} added successfully`
            clearAddForm()
        }
    })
}


// Edit inventory item
function editItem(id) {
    fetch(`/inventory/${id}`)
        .then(res => res.json())
        .then(item => {
            const row = document.querySelector(`button[onclick="editItem(${id})"]`).closest('tr')
            row.innerHTML = `
                <td>${item.id}</td>
                <td><input type="text" id="edit-name-${id}" value="${item.product_name}"></td>
                <td><input type="text" id="edit-brand-${id}" value="${item.brands}"></td>
                <td><input type="number" id="edit-price-${id}" value="${item.price}"></td>
                <td><input type="number" id="edit-stock-${id}" value="${item.stock}"></td>
                <td>
                    <button onclick="saveItem(${id})">💾</button>
                    <button onclick="loadInventory()">✖️</button>
                </td>
            `
        })
}


// Save edited inventory item
function saveItem(id) {
    const item = {
        product_name: document.getElementById(`edit-name-${id}`).value,
        brands: document.getElementById(`edit-brand-${id}`).value,
        price: parseFloat(document.getElementById(`edit-price-${id}`).value),
        stock: parseInt(document.getElementById(`edit-stock-${id}`).value)
    }
    fetch(`/inventory/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
    })
    .then(res => res.json())
    .then(() => loadInventory())
}


// Delete inventory item
function deleteItem(id) {
    fetch(`/inventory/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(() => loadInventory())
}


// Show item detail
function showDetail(id) {
    fetch(`/inventory/${id}`)
        .then(res => res.json())
        .then(item => {
            document.getElementById('detail-name').textContent = item.product_name
            document.getElementById('detail-barcode').textContent = item.barcode
            document.getElementById('detail-brand').textContent = item.brands
            document.getElementById('detail-categories').textContent = item.categories
            document.getElementById('detail-ingredients').textContent = item.ingredients_text
            document.getElementById('detail-grades').textContent = item.nutrition_grades
            document.getElementById('detail-price').textContent = item.price
            document.getElementById('detail-stock').textContent = item.stock
            document.getElementById('item-detail').style.display = 'block'
            document.getElementById('item-detail-overlay').style.display = 'flex'
        })
}


// Close item detail
function closeDetail() {
    document.getElementById('item-detail-overlay').style.display = 'none'
}


// Lookup item from API (Get item)
function lookupItem() {
    const query = document.getElementById('lookup-input').value
    const param = isNaN(query) ? `name=${query}` : `barcode=${query}`
    fetch(`/inventory/lookup?${param}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById('lookup-message').textContent = data.error
                document.getElementById('lookup-table').style.display = 'none'
                document.getElementById('lookup-import').style.display = 'none'
            } else {
                document.getElementById('lookup-message').textContent = ''
                const tbody = document.getElementById('lookup-list')
                tbody.innerHTML = `
                    <tr>
                        <td>${data.product_name}</td>
                        <td>${data.brands}</td>
                        <td>${data.categories}</td>
                        <td>${data.nutrition_grades}</td>
                    </tr>
                `
                document.getElementById('lookup-table').style.display = 'table'
                document.getElementById('lookup-import').style.display = 'block'
                document.getElementById('lookup-input').dataset.barcode = data.barcode
            }
        })
}


// Import item from API into inventory
function importItem() {
    const barcode = document.getElementById('lookup-input').dataset.barcode
    const price = parseFloat(document.getElementById('lookup-price').value)
    const stock = parseInt(document.getElementById('lookup-stock').value)
    fetch('/inventory/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ barcode, price, stock })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('lookup-message').textContent = data.error
        } else {
            document.getElementById('lookup-message').textContent = `${data.product_name} added to inventory`
            document.getElementById('lookup-table').style.display = 'none'
            document.getElementById('lookup-import').style.display = 'none'
            document.getElementById('lookup-input').value = ''
        }
    })
}


// Clear add item form
function clearAddForm() {
    document.getElementById('add-name').value = ''
    document.getElementById('add-brand').value = ''
    document.getElementById('add-barcode').value = ''
    document.getElementById('add-categories').value = ''
    document.getElementById('add-ingredients').value = ''
    document.getElementById('add-grades').value = ''
    document.getElementById('add-price').value = ''
    document.getElementById('add-stock').value = ''
}