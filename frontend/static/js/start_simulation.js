// start_simulation.js

// Initialize the start simulation page
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setupRangeSliders();
});

// Setup event listeners for the form elements
function setupEventListeners() {
    // Update slider value displays for single simulation
    document.getElementById('humanitiesRatio').addEventListener('input', function() {
        document.getElementById('humanitiesValue').textContent = this.value + '%';
        adjustOtherRatios('humanitiesRatio');
    });

    document.getElementById('scienceRatio').addEventListener('input', function() {
        document.getElementById('scienceValue').textContent = this.value + '%';
        adjustOtherRatios('scienceRatio');
    });

    document.getElementById('engineeringRatio').addEventListener('input', function() {
        document.getElementById('engineeringValue').textContent = this.value + '%';
        adjustOtherRatios('engineeringRatio');
    });

    // Update slider value displays for range simulation
    document.getElementById('humanitiesRatioRange').addEventListener('input', function() {
        document.getElementById('humanitiesValueRange').textContent = this.value + '%';
        adjustOtherRatiosRange('humanitiesRatioRange');
    });

    document.getElementById('scienceRatioRange').addEventListener('input', function() {
        document.getElementById('scienceValueRange').textContent = this.value + '%';
        adjustOtherRatiosRange('scienceRatioRange');
    });

    document.getElementById('engineeringRatioRange').addEventListener('input', function() {
        document.getElementById('engineeringValueRange').textContent = this.value + '%';
        adjustOtherRatiosRange('engineeringRatioRange');
    });

    // Single simulation button
    document.getElementById('startSingleBtn').addEventListener('click', function() {
        startSingleSimulation();
    });

    // Range simulation button
    document.getElementById('startRangeBtn').addEventListener('click', function() {
        startRangeSimulation();
    });
}

// Adjust other ratios when one changes to maintain 100% total for single simulation
function adjustOtherRatios(changedId) {
    const humanitiesSlider = document.getElementById('humanitiesRatio');
    const scienceSlider = document.getElementById('scienceRatio');
    const engineeringSlider = document.getElementById('engineeringRatio');
    
    const humanitiesValue = parseInt(humanitiesSlider.value);
    const scienceValue = parseInt(scienceSlider.value);
    const engineeringValue = parseInt(engineeringSlider.value);
    
    const total = humanitiesValue + scienceValue + engineeringValue;
    
    if (total > 100) {
        // Adjust the non-changed sliders proportionally
        switch(changedId) {
            case 'humanitiesRatio':
                const remainingAfterHumanities = 100 - humanitiesValue;
                const scienceProportion = (scienceValue / (scienceValue + engineeringValue)) * remainingAfterHumanities;
                const engineeringProportion = (engineeringValue / (scienceValue + engineeringValue)) * remainingAfterHumanities;
                scienceSlider.value = Math.round(scienceProportion);
                engineeringSlider.value = 100 - humanitiesValue - Math.round(scienceProportion);
                document.getElementById('scienceValue').textContent = Math.round(scienceProportion) + '%';
                document.getElementById('engineeringValue').textContent = (100 - humanitiesValue - Math.round(scienceProportion)) + '%';
                break;
            case 'scienceRatio':
                const remainingAfterScience = 100 - scienceValue;
                const humanitiesProportion = (humanitiesValue / (humanitiesValue + engineeringValue)) * remainingAfterScience;
                const engineeringProportion2 = (engineeringValue / (humanitiesValue + engineeringValue)) * remainingAfterScience;
                humanitiesSlider.value = Math.round(humanitiesProportion);
                engineeringSlider.value = 100 - scienceValue - Math.round(humanitiesProportion);
                document.getElementById('humanitiesValue').textContent = Math.round(humanitiesProportion) + '%';
                document.getElementById('engineeringValue').textContent = (100 - scienceValue - Math.round(humanitiesProportion)) + '%';
                break;
            case 'engineeringRatio':
                const remainingAfterEngineering = 100 - engineeringValue;
                const humanitiesProportion2 = (humanitiesValue / (humanitiesValue + scienceValue)) * remainingAfterEngineering;
                const scienceProportion2 = (scienceValue / (humanitiesValue + scienceValue)) * remainingAfterEngineering;
                humanitiesSlider.value = Math.round(humanitiesProportion2);
                scienceSlider.value = 100 - engineeringValue - Math.round(humanitiesProportion2);
                document.getElementById('humanitiesValue').textContent = Math.round(humanitiesProportion2) + '%';
                document.getElementById('scienceValue').textContent = (100 - engineeringValue - Math.round(humanitiesProportion2)) + '%';
                break;
        }
    }
}

// Adjust other ratios when one changes to maintain 100% total for range simulation
function adjustOtherRatiosRange(changedId) {
    const humanitiesSlider = document.getElementById('humanitiesRatioRange');
    const scienceSlider = document.getElementById('scienceRatioRange');
    const engineeringSlider = document.getElementById('engineeringRatioRange');
    
    const humanitiesValue = parseInt(humanitiesSlider.value);
    const scienceValue = parseInt(scienceSlider.value);
    const engineeringValue = parseInt(engineeringSlider.value);
    
    const total = humanitiesValue + scienceValue + engineeringValue;
    
    if (total > 100) {
        // Adjust the non-changed sliders proportionally
        switch(changedId) {
            case 'humanitiesRatioRange':
                const remainingAfterHumanities = 100 - humanitiesValue;
                const scienceProportion = (scienceValue / (scienceValue + engineeringValue)) * remainingAfterHumanities;
                const engineeringProportion = (engineeringValue / (scienceValue + engineeringValue)) * remainingAfterHumanities;
                scienceSlider.value = Math.round(scienceProportion);
                engineeringSlider.value = 100 - humanitiesValue - Math.round(scienceProportion);
                document.getElementById('scienceValueRange').textContent = Math.round(scienceProportion) + '%';
                document.getElementById('engineeringValueRange').textContent = (100 - humanitiesValue - Math.round(scienceProportion)) + '%';
                break;
            case 'scienceRatioRange':
                const remainingAfterScience = 100 - scienceValue;
                const humanitiesProportion = (humanitiesValue / (humanitiesValue + engineeringValue)) * remainingAfterScience;
                const engineeringProportion2 = (engineeringValue / (humanitiesValue + engineeringValue)) * remainingAfterScience;
                humanitiesSlider.value = Math.round(humanitiesProportion);
                engineeringSlider.value = 100 - scienceValue - Math.round(humanitiesProportion);
                document.getElementById('humanitiesValueRange').textContent = Math.round(humanitiesProportion) + '%';
                document.getElementById('engineeringValueRange').textContent = (100 - scienceValue - Math.round(humanitiesProportion)) + '%';
                break;
            case 'engineeringRatioRange':
                const remainingAfterEngineering = 100 - engineeringValue;
                const humanitiesProportion2 = (humanitiesValue / (humanitiesValue + scienceValue)) * remainingAfterEngineering;
                const scienceProportion2 = (scienceValue / (humanitiesValue + scienceValue)) * remainingAfterEngineering;
                humanitiesSlider.value = Math.round(humanitiesProportion2);
                scienceSlider.value = 100 - engineeringValue - Math.round(humanitiesProportion2);
                document.getElementById('humanitiesValueRange').textContent = Math.round(humanitiesProportion2) + '%';
                document.getElementById('scienceValueRange').textContent = (100 - engineeringValue - Math.round(humanitiesProportion2)) + '%';
                break;
        }
    }
}

// Setup range sliders
function setupRangeSliders() {
    // Initialize display values for single simulation
    document.getElementById('humanitiesValue').textContent = document.getElementById('humanitiesRatio').value + '%';
    document.getElementById('scienceValue').textContent = document.getElementById('scienceRatio').value + '%';
    document.getElementById('engineeringValue').textContent = document.getElementById('engineeringRatio').value + '%';
    
    // Initialize display values for range simulation
    document.getElementById('humanitiesValueRange').textContent = document.getElementById('humanitiesRatioRange').value + '%';
    document.getElementById('scienceValueRange').textContent = document.getElementById('scienceRatioRange').value + '%';
    document.getElementById('engineeringValueRange').textContent = document.getElementById('engineeringRatioRange').value + '%';
}

// Start a single simulation
function startSingleSimulation() {
    // Get form values for single simulation
    const formData = {
        rows: parseInt(document.getElementById('rows').value),
        cols: parseInt(document.getElementById('cols').value),
        totalStudents: parseInt(document.getElementById('totalStudents').value),
        humanitiesRatio: parseInt(document.getElementById('humanitiesRatio').value),
        scienceRatio: parseInt(document.getElementById('scienceRatio').value),
        engineeringRatio: parseInt(document.getElementById('engineeringRatio').value),
        cleaningTime: parseInt(document.getElementById('cleaningTime').value),
        useMultiprocessing: document.getElementById('useMultiprocessing').checked
    };

    // Validate inputs
    if (formData.rows <= 0 || formData.cols <= 0) {
        alert('Rows and columns must be positive numbers');
        return;
    }
    
    if (formData.totalStudents <= 0) {
        alert('Total students must be a positive number');
        return;
    }

    // Update progress
    updateProgress(0, 'Starting simulation...');
    
    // Make API call
    fetch('/api/start_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        // Check if response is ok (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            updateProgress(100, 'Simulation completed successfully!');
        } else {
            updateProgress(0, 'Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        updateProgress(0, 'Error occurred: ' + error.message);
    });
}

// Start a range simulation
function startRangeSimulation() {
    // Get form values for range simulation
    const formData = {
        rows: parseInt(document.getElementById('rangeRows').value),
        cols: parseInt(document.getElementById('rangeCols').value),
        minStudents: parseInt(document.getElementById('minStudents').value),
        maxStudents: parseInt(document.getElementById('maxStudents').value),
        studentStep: parseInt(document.getElementById('studentStep').value),
        repeatCount: parseInt(document.getElementById('repeatCount').value),
        humanitiesRatio: parseInt(document.getElementById('humanitiesRatioRange').value),
        scienceRatio: parseInt(document.getElementById('scienceRatioRange').value),
        engineeringRatio: parseInt(document.getElementById('engineeringRatioRange').value),
        cleaningTime: parseInt(document.getElementById('cleaningTimeRange').value),
        useMultiprocessing: document.getElementById('useMultiprocessingRange').checked
    };

    // Validate inputs
    if (formData.rows <= 0 || formData.cols <= 0) {
        alert('Rows and columns must be positive numbers');
        return;
    }
    
    if (formData.minStudents <= 0 || formData.maxStudents <= 0) {
        alert('Min and max students must be positive numbers');
        return;
    }
    
    if (formData.minStudents > formData.maxStudents) {
        alert('Minimum students cannot be greater than maximum students');
        return;
    }
    
    if (formData.studentStep <= 0) {
        alert('Student step must be a positive number');
        return;
    }

    // Show range simulation info section
    document.getElementById('rangeSimulationInfo').style.display = 'block';
    document.getElementById('rangeProgressList').innerHTML = '';

    // Calculate total simulations
    const totalSimulations = Math.ceil((formData.maxStudents - formData.minStudents + 1) / formData.studentStep) * formData.repeatCount;
    
    // Update progress
    updateProgress(0, `Starting range simulation: ${totalSimulations} total runs`);
    
    // Make API call for range simulation
    fetch('/api/start_range_simulation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        // Check if response is ok (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'error') {
            updateProgress(0, 'Error: ' + data.message);
        } else {
            updateProgress(100, data.message);
            
            // Update range progress list with results
            if (data.results) {
                document.getElementById('rangeProgressList').innerHTML = '';
                data.results.forEach((result, index) => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    listItem.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <span>Run ${index+1}: ${result.students} students</span>
                            <span class="badge bg-success">Completed</span>
                        </div>
                    `;
                    document.getElementById('rangeProgressList').appendChild(listItem);
                });
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        updateProgress(0, 'Error occurred: ' + error.message);
    });
}

// Update progress display
function updateProgress(percent, message) {
    const progressBar = document.getElementById('progressBar');
    const progressInfo = document.getElementById('progressInfo');
    
    if (progressBar) {
        progressBar.style.width = percent + '%';
        progressBar.textContent = percent + '%';
    }
    
    if (progressInfo) {
        progressInfo.innerHTML = `<p>${message}</p>`;
    }
}