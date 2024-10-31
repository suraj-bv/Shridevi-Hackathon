const apiUrl = 'http://127.0.0.1:5000/api/equipment';

// Fetch and display equipment data
async function fetchEquipmentData() {
    const response = await fetch(apiUrl);
    const equipmentList = await response.json();
    renderEquipmentList(equipmentList);
}

// Add a new equipment record
async function addEquipment() {
    const name = document.getElementById('equipmentName').value;
    const type = document.getElementById('equipmentType').value;
    const quantity = document.getElementById('equipmentQuantity').value;
    const price_per_day = document.getElementById('equipmentPrice').value;

    if (name && type && quantity && price_per_day) {
        const newEquipment = { name, type, quantity: parseInt(quantity), price_per_day: parseFloat(price_per_day) };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newEquipment)
        });

        if (response.ok) {
            resetEquipmentForm();
            fetchEquipmentData();
        }
    } else {
        alert('Please fill all fields');
    }
}

// Display equipment records in table
function renderEquipmentList(equipmentList) {
    const tableBody = document.querySelector('#equipmentTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    equipmentList.forEach((equipment) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${equipment.name}</td>
            <td>${equipment.type}</td>
            <td>${equipment.quantity}</td>
            <td>${equipment.price_per_day}</td>
            <td><button onclick="deleteEquipment(${equipment.id})">Delete</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Delete equipment record
async function deleteEquipment(id) {
    await fetch(`${apiUrl}/${id}`, {
        method: 'DELETE'
    });
    fetchEquipmentData();
}

// Reset form
function resetEquipmentForm() {
    document.getElementById('equipmentName').value = '';
    document.getElementById('equipmentType').value = '';
    document.getElementById('equipmentQuantity').value = '';
    document.getElementById('equipmentPrice').value = '';
}

// Initialize data fetch on page load
document.addEventListener('DOMContentLoaded', fetchEquipmentData);
