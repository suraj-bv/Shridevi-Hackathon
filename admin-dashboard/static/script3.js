const apiUrl = 'http://127.0.0.1:5000/api/schemes';

// Fetch and display scheme data
async function fetchSchemeData() {
    const response = await fetch(apiUrl);
    const schemeList = await response.json();
    renderSchemeList(schemeList);
}

// Add a new scheme record
async function addScheme() {
    const name = document.getElementById('schemeName').value;
    const description = document.getElementById('schemeDescription').value;
    const apply_link = document.getElementById('schemeApplyLink').value;
    const eligibility_criteria = document.getElementById('schemeEligibility').value;

    if (name && description && apply_link && eligibility_criteria) {
        const newScheme = { name, description, apply_link, eligibility_criteria };

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newScheme)
        });

        if (response.ok) {
            resetSchemeForm();
            fetchSchemeData();
        }
    } else {
        alert('Please fill all fields');
    }
}

// Display scheme records in table
function renderSchemeList(schemeList) {
    const tableBody = document.querySelector('#schemesTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    schemeList.forEach((scheme) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${scheme.name}</td>
            <td>${scheme.description}</td>
            <td><a href="${scheme.apply_link}" target="_blank">${scheme.apply_link}</a></td>
            <td>${scheme.eligibility_criteria}</td>
            <td><button onclick="deleteScheme(${scheme.id})">Delete</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Delete scheme record
async function deleteScheme(id) {
    await fetch(`${apiUrl}/${id}`, {
        method: 'DELETE'
    });
    fetchSchemeData();
}

// Reset form
function resetSchemeForm() {
    document.getElementById('schemeName').value = '';
    document.getElementById('schemeDescription').value = '';
    document.getElementById('schemeApplyLink').value = '';
    document.getElementById('schemeEligibility').value = '';
}

// Initialize data fetch on page load
document.addEventListener('DOMContentLoaded', fetchSchemeData);
