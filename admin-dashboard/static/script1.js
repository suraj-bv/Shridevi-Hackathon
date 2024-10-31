const apiUrl = 'http://127.0.0.1:5000/api/labor';

// Fetch and display labor data
async function fetchLaborData() {
    const response = await fetch(apiUrl);
    const laborList = await response.json();
    renderLaborList(laborList);
}

// Add a new labor record with validation
async function addLabor() {
    const name = document.getElementById('laborName').value;
    const age = document.getElementById('laborAge').value;
    const contact_no = document.getElementById('laborContact').value;
    const address = document.getElementById('laborAddress').value;

    // Validate contact number: ensure it's exactly 10 digits and contains only numbers
    const contactPattern = /^\d{10}$/;
    if (!contactPattern.test(contact_no)) {
        alert("Contact number must be exactly 10 digits and contain only numbers.");
        return;
    }

    if (name && age && contact_no && address) {
        const newLabor = { name, age: parseInt(age), contact_no, address };
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newLabor)
        });

        if (response.ok) {
            resetLaborForm();
            fetchLaborData();
        }
    } else {
        alert('Please fill all fields');
    }
}

// Display labor records in table
function renderLaborList(laborList) {
    const tableBody = document.querySelector('#laborTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    laborList.forEach((labor) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${labor.name}</td>
            <td>${labor.age}</td>
            <td>${labor.contact_no}</td>
            <td>${labor.address}</td>
            <td><button onclick="deleteLabor(${labor.id})">Delete</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Delete labor record
async function deleteLabor(id) {
    await fetch(`${apiUrl}/${id}`, {
        method: 'DELETE'
    });
    fetchLaborData();
}

// Reset form
function resetLaborForm() {
    document.getElementById('laborName').value = '';
    document.getElementById('laborAge').value = '';
    document.getElementById('laborContact').value = '';
    document.getElementById('laborAddress').value = '';
}

// Initialize data fetch on page load
document.addEventListener('DOMContentLoaded', fetchLaborData);
