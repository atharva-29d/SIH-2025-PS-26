// Define the base URL for our backend API
const API_BASE_URL = 'http://127.0.0.1:8000';

// Dummy data for login and patient list
const doctors = [{ username: "anjali", password: "123", name: "Dr. Anjali Sharma", specialty: "Ayurveda" }];
const patients = [{ id: 101, name: 'Rajesh Kumar', age: 45, gender: 'Male', lastVisit: '2025-08-20' }];

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const welcomeMessage = document.getElementById('welcomeMessage');
    if (welcomeMessage) {
        initializeDashboard();
    }
});

function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const doctor = doctors.find(d => d.username === username && d.password === password);

    if (doctor) {
        sessionStorage.setItem('doctor', JSON.stringify(doctor));
        window.location.href = 'dashboard.html';
    } else {
        document.getElementById('loginError').style.display = "block";
    }
}

function initializeDashboard() {
    const doctor = JSON.parse(sessionStorage.getItem('doctor'));
    if (!doctor) {
        window.location.href = 'index.html';
        return;
    }

    document.getElementById('welcomeMessage').textContent = `Welcome, ${doctor.name}`;
    populateDoctorInfo(doctor.name, doctor.specialty);
    populatePatientList();

    const searchInput = document.getElementById('searchInput');
    const resultsContainer = document.getElementById('resultsContainer');
    searchInput.addEventListener('keyup', async () => {
        const query = searchInput.value;
        if (query.length < 3) {
            resultsContainer.innerHTML = '';
            return;
        }
        try {
            const response = await fetch(`${API_BASE_URL}/api/search-all?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = '<p class="error">Could not fetch results.</p>';
        }
    });

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            sessionStorage.clear();
            window.location.href = 'index.html';
        });
    }
}

function populateDoctorInfo(name, specialty) {
    const doctorInfoDiv = document.getElementById('doctorInfo');
    if (doctorInfoDiv) {
        doctorInfoDiv.innerHTML = `<p><strong>Name:</strong> ${name}</p><p><strong>Specialty:</strong> ${specialty}</p>`;
    }
}

function populatePatientList() {
    const tbody = document.querySelector('#patientList tbody');
    if (!tbody) return;
    tbody.innerHTML = '';
    patients.forEach(patient => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${patient.id}</td><td>${patient.name}</td><td>${patient.age}</td><td>${patient.gender}</td><td>${patient.lastVisit}</td>`;
        row.addEventListener('click', () => {
            document.getElementById('selectedPatient').textContent = `Selected Patient: ${patient.name} (ID: ${patient.id})`;
        });
        tbody.appendChild(row);
    });
}

function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    let html = "";

    // GHO Section
    if (data.gho && data.gho.length > 0) {
      html += "<h2>GHO Indicators</h2>";
      data.gho.forEach(ind => {
        html += `<div class="result-item">
                   <strong>${ind.IndicatorName}</strong> (${ind.Code})
                   <button onclick="fetchWHOData('${ind.Code}')">View Data</button>
                 </div>`;
      });
    }

    // ICD-11 Section
    if (data.icd11 && data.icd11.length > 0) {
      html += "<h2>ICD-11 / TM11 Codes</h2>";
      data.icd11.forEach(ent => {
        const title = ent.title.replace(/<[^>]*>/g, '');
        const code = ent.id.split('/').pop();
        html += `<div class="result-item">
                   <strong>${title}</strong> (${code})
                   <button onclick="viewICDDetails('${ent.id}')">View JSON</button>
                 </div>`;
      });
    }

    if (!html) html = "<p>No results found for your query.</p>";
    resultsContainer.innerHTML = html;
}

async function fetchWHOData(code) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "Loading GHO data for " + code + "...";
    try {
        const res = await fetch(`/api/who-data?query=${code}`);
        const data = await res.json();
        resultsContainer.innerHTML = `<h3>Data for ${code}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (err) {
        resultsContainer.textContent = "Error fetching GHO data: " + err;
    }
}

async function viewICDDetails(uri) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "Loading ICD-11 details for " + uri.split('/').pop() + "...";
    try {
        const res = await fetch(`/api/icd-details?uri=${encodeURIComponent(uri)}`);
        const data = await res.json();
        resultsContainer.innerHTML = `<h3>Details for ${uri.split('/').pop()}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (err) {
        resultsContainer.textContent = "Error fetching ICD-11 details: " + err;
    }
}