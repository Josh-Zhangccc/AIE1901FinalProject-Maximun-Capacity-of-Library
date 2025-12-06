// simulation_records.js

// Initialize the simulation records page
document.addEventListener('DOMContentLoaded', function() {
    loadSimulationRecords();
    setupEventListeners();
});

// Load simulation records
function loadSimulationRecords() {
    fetch('/api/simulation_records')
    .then(response => response.json())
    .then(records => {
        // Load file tree
        loadFileTree(records);
        
        // Load recent simulations table
        loadRecentSimulationsTable(records);
    })
    .catch(error => {
        console.error('Error loading simulation records:', error);
        
        // Show error in both areas
        document.getElementById('fileTree').innerHTML = '<p>Error loading file tree.</p>';
        document.getElementById('recentSimulationsTable').innerHTML = '<tr><td colspan="5">Error loading recent simulations.</td></tr>';
    });
}

// Load the file tree structure
function loadFileTree(records) {
    // For demo purposes, create a simple representation
    // In a real implementation, we would create a proper tree structure
    
    let treeHtml = '<div class="file-tree"><div class="file-node">';
    treeHtml += '<div><i class="folder-icon">📁</i> simulation_data/</div>';
    treeHtml += '<div class="file-node"><i class="folder-icon">📁</i> figures/</div>';
    treeHtml += '<div class="file-node"><i class="folder-icon">📁</i> simulations/</div>';
    
    // Add simulation files to the tree
    if (records.length > 0) {
        records.slice(0, 5).forEach(record => { // Show only first 5 for demo
            treeHtml += `<div class="file-node"><i class="file-icon">📄</i> ${record.name}</div>`;
        });
        
        if (records.length > 5) {
            treeHtml += `<div class="file-node">... and ${records.length - 5} more files</div>`;
        }
    } else {
        treeHtml += '<div class="file-node">No simulation files found</div>';
    }
    
    treeHtml += '</div></div>';
    
    document.getElementById('fileTree').innerHTML = treeHtml;
}

// Load recent simulations table
function loadRecentSimulationsTable(records) {
    const tableBody = document.getElementById('recentSimulationsTable');
    tableBody.innerHTML = '';
    
    if (records.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5">No simulation records found.</td></tr>';
        return;
    }
    
    // Sort by modification date (in a real implementation, we would get this from the backend)
    const sortedRecords = records.slice(0, 10); // Show only first 10 for demo
    
    sortedRecords.forEach(record => {
        // For demo purposes, create a fake modification date
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30)); // Random date in last 30 days
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${record.name}</td>
            <td>${record.path}</td>
            <td>${(Math.random() * 100).toFixed(1)} KB</td>
            <td>${date.toLocaleDateString()}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="loadSimulation('${record.path}')">Load</button>
                <button class="btn btn-sm btn-info" onclick="viewPlotForSimulation('${record.path}')">View Plot</button>
                <button class="btn btn-sm btn-danger" onclick="deleteSimulation('${record.path}')">Delete</button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Refresh button
    document.getElementById('refreshRecordsBtn').addEventListener('click', function() {
        loadSimulationRecords();
    });
}

// Load a specific simulation (stub function)
function loadSimulation(path) {
    alert(`Loading simulation: ${path}\nIn a real implementation, this would load the simulation data.`);
}

// View plot for a simulation (stub function)
function viewPlotForSimulation(path) {
    alert(`Viewing plot for simulation: ${path}\nIn a real implementation, this would generate or show plots for the simulation.`);
}

// Delete a simulation (stub function)
function deleteSimulation(path) {
    if (confirm(`Are you sure you want to delete the simulation: ${path}?`)) {
        alert(`Deleting simulation: ${path}\nIn a real implementation, this would delete the simulation file.`);
    }
}
