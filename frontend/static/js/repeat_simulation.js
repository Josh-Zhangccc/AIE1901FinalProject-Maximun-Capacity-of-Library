// repeat_simulation.js

// Initialize the repeat simulation page
document.addEventListener('DOMContentLoaded', function() {
    loadSeatCounts();
    setupEventListeners();
});

// Load seat counts (folders) from the API
function loadSeatCounts() {
    fetch('/api/seat_counts')
    .then(response => response.json())
    .then(seatCounts => {
        const selectElement = document.getElementById('seatCountSelect');
        selectElement.innerHTML = '';
        
        if (seatCounts.length === 0) {
            const option = document.createElement('option');
            option.text = 'No seat counts found';
            selectElement.appendChild(option);
        } else {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select seat count';
            selectElement.appendChild(defaultOption);
            
            seatCounts.forEach(seatCount => {
                const option = document.createElement('option');
                option.value = seatCount.value;
                option.text = seatCount.label;
                selectElement.appendChild(option);
            });
        }
    })
    .catch(error => {
        console.error('Error loading seat counts:', error);
        const selectElement = document.getElementById('seatCountSelect');
        selectElement.innerHTML = '<option value="">Error loading seat counts</option>';
    });
}

// Load student files for a selected seat count
function loadStudentFiles(seatFolder) {
    fetch(`/api/student_files/${seatFolder}`)
    .then(response => response.json())
    .then(studentFiles => {
        const selectElement = document.getElementById('studentCountSelect');
        selectElement.innerHTML = '';
        selectElement.disabled = false;
        
        if (studentFiles.length === 0) {
            const option = document.createElement('option');
            option.text = 'No student files found';
            selectElement.appendChild(option);
        } else {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select student count';
            selectElement.appendChild(defaultOption);
            
            studentFiles.forEach(file => {
                const option = document.createElement('option');
                option.value = file.path;
                option.text = `[${file.student_count} students] ${file.name}`;
                selectElement.appendChild(option);
            });
        }
    })
    .catch(error => {
        console.error('Error loading student files:', error);
        const selectElement = document.getElementById('studentCountSelect');
        selectElement.innerHTML = '<option value="">Error loading student files</option>';
        selectElement.disabled = false;
    });
}

// Setup event listeners for the page
function setupEventListeners() {
    // Seat count selection change
    document.getElementById('seatCountSelect').addEventListener('change', function() {
        const selectedSeatCount = this.value;
        const studentSelect = document.getElementById('studentCountSelect');
        
        if (selectedSeatCount) {
            loadStudentFiles(selectedSeatCount);
            studentSelect.disabled = false;
        } else {
            studentSelect.disabled = true;
            studentSelect.innerHTML = '<option value="">Please select seat count first</option>';
        }
    });
    
    // Student count selection change
    document.getElementById('studentCountSelect').addEventListener('change', function() {
        const selectedPath = this.value;
        if (selectedPath) {
            document.getElementById('loadRecordBtn').disabled = false;
        } else {
            document.getElementById('loadRecordBtn').disabled = true;
        }
    });
    
    // Load record button
    document.getElementById('loadRecordBtn').addEventListener('click', function() {
        loadSelectedRecord();
    });
    
    // Start repeat simulation button
    document.getElementById('startRepeatBtn').addEventListener('click', function() {
        startRepeatSimulation();
    });
    
    // Pause button
    document.getElementById('pauseBtn').addEventListener('click', function() {
        pauseSimulation();
    });
    
    // Stop button
    document.getElementById('stopBtn').addEventListener('click', function() {
        stopSimulation();
    });
}

// Load selected simulation record
function loadSelectedRecord() {
    const selectedPath = document.getElementById('studentCountSelect').value;
    
    if (!selectedPath) {
        alert('Please select a student count file');
        return;
    }
    
    // Load the JSON file and extract parameters
    loadSimulationData(selectedPath);
}

// Load simulation data from selected JSON file
function loadSimulationData(path) {
    // Fetch the actual JSON file content
    fetch(`/simulation_data/simulations/${path}`)
    .then(response => {
        // Check if the response is OK and not HTML (which would indicate an error)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Check if response is JSON (not HTML error page)
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error('Response is not JSON');
        }
        
        return response.json();
    })
    .then(data => {
        // Extract time steps from the loaded data
        // The data structure may vary, so we need to handle different formats
        let timeSteps = [];
        
        // If data has a specific structure with initial config and time steps
        if (Array.isArray(data)) {
            timeSteps = data;
        } else if (data && typeof data === 'object') {
            // If data contains a time_steps property
            if (data.time_steps && Array.isArray(data.time_steps)) {
                timeSteps = data.time_steps;
            } else {
                // If the entire data object is the time steps array
                timeSteps = Object.values(data);
            }
        }
        
        if (timeSteps.length > 0) {
            // Store the time steps for later use
            window.simulationTimeSteps = timeSteps;
            window.currentStepIndex = 0;
            
            // Extract configuration data if available (first element might be config)
            let configData = null;
            if (timeSteps.length > 0 && timeSteps[0].hasOwnProperty('test_name')) {
                configData = timeSteps[0];
            }
            
            // Show seat visualization and populate with initial data
            document.getElementById('seatVisualization').style.display = 'block';
            
            // Generate seat grid based on initial state
            const firstStep = timeSteps[0];
            if (firstStep.seats_taken_state) {
                generateSeatGridFromState(firstStep.seats_taken_state);
            } else {
                // Fallback to default 3x3 grid if no state data
                generateSeatGrid(3, 3, {});
            }
            
            // Update time display
            document.getElementById('currentTime').textContent = firstStep.time || '7:00';
            
            // Update status indicators
            document.getElementById('occupiedSeats').textContent = firstStep.taken_rate ? 
                firstStep.taken_rate.split(' ')[1].replace('(', '').replace(')', '').replace('%', '') : '0';
            document.getElementById('reservedSeats').textContent = firstStep.reversed_seats || 0;
            
            // Update simulation parameters if config data is available
            if (configData && configData.test_scale) {
                const scale = configData.test_scale;
                const parts = scale.split("->");
                const gridInfo = parts[0]; // e.g., "3*3"
                const studentCount = parts[1]; // e.g., "9"
                
                document.getElementById('simulationParams').innerHTML = `
                    <p><strong>Grid Size:</strong> ${gridInfo}</p>
                    <p><strong>Total Seats:</strong> ${gridInfo.split('*')[0] * gridInfo.split('*')[1]}</p>
                    <p><strong>Total Students:</strong> ${studentCount}</p>
                `;
            } else {
                // Fallback parameters
                document.getElementById('simulationParams').innerHTML = `
                    <p><strong>Grid Size:</strong> 3 x 3</p>
                    <p><strong>Total Seats:</strong> 9</p>
                    <p><strong>Total Students:</strong> 9</p>
                `;
            }
            
            // Update progress info
            document.getElementById('progressInfo').innerHTML = `<p>Loaded simulation record: ${path}</p>`;
            
            // Enable start button
            document.getElementById('startRepeatBtn').disabled = false;
        } else {
            console.error('Error loading simulation data: No time steps found');
            document.getElementById('progressInfo').innerHTML = `<p style="color: red;">Error: No simulation data found in file</p>`;
        }
    })
    .catch(error => {
        console.error('Error loading simulation data:', error);
        document.getElementById('progressInfo').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });
}

// Generate seat grid from state data
function generateSeatGridFromState(state) {
    // Determine grid size from the state keys (e.g. "0,0", "0,1", etc.)
    let maxRow = 0;
    let maxCol = 0;
    
    for (const coordinate in state) {
        if (coordinate.includes(',')) {
            const [row, col] = coordinate.split(',').map(Number);
            maxRow = Math.max(maxRow, row);
            maxCol = Math.max(maxCol, col);
        }
    }
    
    const rows = maxRow + 1;
    const cols = maxCol + 1;
    
    generateSeatGrid(rows, cols, state);
}

// Generate seat grid visualization
function generateSeatGrid(rows, cols, state = {}) {
    const seatGrid = document.getElementById('seatGrid');
    seatGrid.innerHTML = '';
    
    // Set grid layout based on rows and cols
    seatGrid.style.gridTemplateColumns = `repeat(${cols}, minmax(60px, 1fr))`;
    
    // Create seats
    for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
            const coordinate = `${row},${col}`;
            const seatStatus = state[coordinate] || 'V'; // Default to vacant
            
            // Map status codes to CSS classes
            let statusClass, statusText;
            switch(seatStatus) {
                case 'V':
                    statusClass = 'vacant';
                    statusText = 'Vacant';
                    break;
                case 'T':
                    statusClass = 'taken';
                    statusText = 'Taken';
                    break;
                case 'R':
                    statusClass = 'reserved';
                    statusText = 'Reserved';
                    break;
                case 'S':
                    statusClass = 'signed';
                    statusText = 'Signed';
                    break;
                default:
                    statusClass = 'vacant';
                    statusText = 'Vacant';
            }
            
            const seat = document.createElement('div');
            seat.className = `seat ${statusClass}`;
            seat.title = `Seat (${row},${col}): ${statusText}`;
            
            // Add seat coordinates
            const seatCoords = document.createElement('div');
            seatCoords.textContent = `${row},${col}`;
            seatCoords.className = 'seat-coords';
            seat.appendChild(seatCoords);
            
            // Add info indicator
            const info = document.createElement('div');
            info.className = 'seat-info';
            info.textContent = statusText.charAt(0).toUpperCase();
            seat.appendChild(info);
            
            seatGrid.appendChild(seat);
        }
    }
}

// Start repeat simulation
function startRepeatSimulation() {
    if (!window.simulationTimeSteps || window.simulationTimeSteps.length === 0) {
        alert('No simulation data loaded');
        return;
    }
    
    const repeatCount = parseInt(document.getElementById('repeatCount').value);
    if (isNaN(repeatCount) || repeatCount < 1) {
        alert('Please enter a valid repeat count (minimum 1)');
        return;
    }
    
    // Update UI elements
    document.getElementById('startRepeatBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    document.getElementById('stopBtn').disabled = false;
    
    // Reset to first step and start the simulation process
    window.currentStepIndex = 0;
    window.simulationInterval = setInterval(showNextStep, 1000); // 15分钟模拟间隔，这里改为1秒以便演示
}

// Show next step in the simulation
function showNextStep() {
    if (!window.simulationTimeSteps || window.currentStepIndex >= window.simulationTimeSteps.length) {
        // Reached the end of simulation data
        clearInterval(window.simulationInterval);
        document.getElementById('progressInfo').innerHTML = `<p>Simulation completed</p>`;
        
        // Re-enable buttons
        document.getElementById('startRepeatBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('stopBtn').disabled = true;
        return;
    }
    
    const currentStep = window.simulationTimeSteps[window.currentStepIndex];
    
    // Update UI with current step data
    if (currentStep.seats_taken_state) {
        generateSeatGridFromState(currentStep.seats_taken_state);
    }
    
    // Update time display
    document.getElementById('currentTime').textContent = currentStep.time || '7:00';
    
    // Update status indicators
    document.getElementById('occupiedSeats').textContent = currentStep.taken_rate ? 
        currentStep.taken_rate.split(' ')[1].replace('(', '').replace(')', '').replace('%', '') : '0';
    document.getElementById('reservedSeats').textContent = currentStep.reversed_seats || 0;
    
    // Update progress bar
    const progressPercent = (window.currentStepIndex / window.simulationTimeSteps.length) * 100;
    document.getElementById('progressBar').style.width = `${progressPercent}%`;
    document.getElementById('progressBar').textContent = `${Math.round(progressPercent)}%`;
    
    // Update step counter
    document.getElementById('currentIteration').textContent = window.currentStepIndex + 1;
    document.getElementById('totalIterations').textContent = window.simulationTimeSteps.length;
    
    // Move to next step
    window.currentStepIndex++;
}

// Pause simulation
function pauseSimulation() {
    if (window.simulationInterval) {
        clearInterval(window.simulationInterval);
        window.simulationInterval = null;
        
        // Update button states
        document.getElementById('startRepeatBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
    }
}

// Stop simulation
function stopSimulation() {
    if (window.simulationInterval) {
        clearInterval(window.simulationInterval);
        window.simulationInterval = null;
    }
    
    // Reset UI
    document.getElementById('startRepeatBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('stopBtn').disabled = true;
    
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressBar').textContent = '0%';
    document.getElementById('progressInfo').innerHTML = '<p>Simulation stopped</p>';
    
    document.getElementById('currentIteration').textContent = '0';
    window.currentStepIndex = 0;
}