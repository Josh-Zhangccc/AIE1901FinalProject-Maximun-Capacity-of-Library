// view_plots.js

// Initialize the view plots page
document.addEventListener('DOMContentLoaded', function() {
    loadSeatCountsForPlot();
    loadAvailablePlots();
    setupEventListeners();
});

// Load seat counts for plot generation
function loadSeatCountsForPlot() {
    fetch('/api/seat_counts')
    .then(response => response.json())
    .then(seatCounts => {
        const selectElement = document.getElementById('seatCountForPlot');
        selectElement.innerHTML = '';
        
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
    })
    .catch(error => {
        console.error('Error loading seat counts:', error);
        const selectElement = document.getElementById('seatCountForPlot');
        selectElement.innerHTML = '<option value="">Error loading seat counts</option>';
    });
}

// Load student files for a selected seat count
function loadStudentFilesForPlot(seatFolder) {
    fetch(`/api/student_files/${seatFolder}`)
    .then(response => response.json())
    .then(studentFiles => {
        const selectElement = document.getElementById('studentCountForPlot');
        selectElement.innerHTML = '';
        selectElement.disabled = false;
        
        // Get unique student counts
        const uniqueStudentCounts = [...new Set(studentFiles.map(file => file.student_count))];
        uniqueStudentCounts.sort((a, b) => a - b);
        
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.text = 'Select student count';
        selectElement.appendChild(defaultOption);
        
        uniqueStudentCounts.forEach(count => {
            const option = document.createElement('option');
            option.value = count;
            option.text = `${count} students`;
            selectElement.appendChild(option);
        });
        
        // Set the range input based on available student counts
        if (uniqueStudentCounts.length > 0) {
            const minCount = Math.min(...uniqueStudentCounts);
            const maxCount = Math.max(...uniqueStudentCounts);
            document.getElementById('studentRange').value = `${minCount}-${maxCount}`;
        }
    })
    .catch(error => {
        console.error('Error loading student files:', error);
        const selectElement = document.getElementById('studentCountForPlot');
        selectElement.innerHTML = '<option value="">Error loading student files</option>';
        selectElement.disabled = false;
    });
}

// Load available plots
function loadAvailablePlots() {
    // Add timestamp to bypass cache
    fetch('/api/plots?' + new Date().getTime())
    .then(response => response.json())
    .then(plots => {
        const plotGallery = document.getElementById('plotGallery');
        plotGallery.innerHTML = '';
        
        if (plots.length === 0) {
            plotGallery.innerHTML = '<div class="col-12"><p>No plots available. Generate some plots first.</p></div>';
            return;
        }
        
        plots.forEach(plot => {
            const plotItem = document.createElement('div');
            plotItem.className = 'col-md-4 col-lg-3 plot-item';
            
            // 确保图像路径正确 - 修复路径处理逻辑
            let imagePath = plot.path;
            // 确保路径不包含重复的路径部分
            if (imagePath.startsWith('/')) {
                imagePath = imagePath.substring(1);  // 移除开头的斜杠
            }
            const fullImagePath = `/simulation_data/figures/${imagePath}?t=${new Date().getTime()}`;
            
            plotItem.innerHTML = `
                <div class="card">
                    <img src="${fullImagePath}" 
                         alt="${plot.name}" 
                         class="card-img-top plot-thumb"
                         loading="lazy"
                         onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'100%\' height=\'200\' viewBox=\'0 0 200 200\'><rect width=\'100%\' height=\'100%\' fill=\'%23f8f9fa\'/><text x=\'50%\' y=\'50%\' dominant-baseline=\'middle\' text-anchor=\'middle\' font-family=\'Arial\' font-size=\'14\' fill=\'%236c757d\'>${encodeURIComponent(plot.name)}</text></svg>'; this.classList.add('placeholder-img');">
                    <div class="card-body">
                        <h6 class="card-title">${plot.name}</h6>
                        <p class="card-text plot-info">${plot.path}</p>
                    </div>
                </div>
            `;
            
            // Add click event to show in modal
            const img = plotItem.querySelector('.plot-thumb');
            img.addEventListener('click', function() {
                showPlotInModal(plot);
            });
            
            plotGallery.appendChild(plotItem);
        });
    })
    .catch(error => {
        console.error('Error loading plots:', error);
        document.getElementById('plotGallery').innerHTML = '<div class="col-12"><p>Error loading plots.</p></div>';
    });
}

// Setup event listeners
function setupEventListeners() {
    // Seat count selection change
    document.getElementById('seatCountForPlot').addEventListener('change', function() {
        const selectedSeatCount = this.value;
        const studentSelect = document.getElementById('studentCountForPlot');
        const plotTypeSelect = document.getElementById('plotType');
        const studentRangeDiv = document.getElementById('studentRangeDiv');
        
        if (selectedSeatCount) {
            loadStudentFilesForPlot(selectedSeatCount);
            plotTypeSelect.disabled = false;
            
            // Reset other fields
            studentSelect.value = '';
            studentSelect.disabled = false;
            document.getElementById('studentRange').value = '';
            document.getElementById('studentRange').disabled = true;
            studentRangeDiv.style.display = 'none';
            
            // Hide existing plots section
            document.getElementById('existingPlotsSection').style.display = 'none';
        } else {
            plotTypeSelect.disabled = true;
            studentSelect.disabled = true;
            studentSelect.innerHTML = '<option value="">Please select seat count first</option>';
            document.getElementById('studentRange').disabled = true;
            document.getElementById('studentRange').value = '';
            studentRangeDiv.style.display = 'none';
        }
    });
    
    // Plot type selection change
    document.getElementById('plotType').addEventListener('change', function() {
        const plotType = this.value;
        const studentCountSelect = document.getElementById('studentCountForPlot');
        const studentRangeDiv = document.getElementById('studentRangeDiv');
        const studentRangeInput = document.getElementById('studentRange');
        
        if (plotType === 'analysis') {
            studentCountSelect.style.display = 'none';
            studentRangeDiv.style.display = 'block';
            studentRangeInput.disabled = false;
        } else {
            studentCountSelect.style.display = 'block';
            studentCountSelect.disabled = false;
            studentRangeDiv.style.display = 'none';
        }
    });
    
    // Generate plot button
    document.getElementById('generatePlotBtn').addEventListener('click', function() {
        generatePlots();
    });
    
    // Check existing plots button
    document.getElementById('checkExistingPlotsBtn').addEventListener('click', function() {
        checkExistingPlots();
    });
    
    // Confirm generation button
    document.getElementById('confirmGenerationBtn').addEventListener('click', function() {
        generatePlots();
        document.getElementById('existingPlotsSection').style.display = 'none';
    });
    
    // Update plot button
    document.getElementById('updatePlotBtn').addEventListener('click', function() {
        generatePlots(true); // Force update
        document.getElementById('existingPlotsSection').style.display = 'none';
    });
    
    // Batch generate button - 一键绘制功能
    document.getElementById('batchGenerateBtn').addEventListener('click', function() {
        batchGeneratePlots();
    });
    
    // Filter by seat count button - 按座位数筛选功能
    document.getElementById('filterBySeatBtn').addEventListener('click', function() {
        filterPlotsBySeatCount();
    });
}

// 批量生成图像功能
function batchGeneratePlots() {
    const seatCount = document.getElementById('seatCountForPlot').value;
    const plotType = document.getElementById('plotType').value;
    
    if (!seatCount) {
        alert('Please select a seat count first');
        return;
    }
    
    let minStudents, maxStudents;
    
    if (plotType === 'analysis') {
        const rangeInput = document.getElementById('studentRange').value;
        if (!rangeInput || !/^\d+-\d+$/.test(rangeInput)) {
            alert('Please enter a valid student range (e.g., 9-19)');
            return;
        }
        [minStudents, maxStudents] = rangeInput.split('-').map(Number);
    } else {
        // For student plots, we'll use the range from available student files
        const studentCount = document.getElementById('studentCountForPlot').value;
        if (!studentCount) {
            alert('Please select a student count or switch to analysis type to enter a range');
            return;
        }
        // We'll auto-detect the range from available student files for the selected seat count
        const seatFolder = document.getElementById('seatCountForPlot').value;
        fetch(`/api/student_files/${seatFolder}`)
        .then(response => response.json())
        .then(studentFiles => {
            const uniqueStudentCounts = [...new Set(studentFiles.map(file => file.student_count))].sort((a, b) => a - b);
            if (uniqueStudentCounts.length > 0) {
                minStudents = Math.min(...uniqueStudentCounts);
                maxStudents = Math.max(...uniqueStudentCounts);
                performBatchGeneration(seatCount, minStudents, maxStudents);
            } else {
                alert('No student simulation data found for selected seat count');
            }
        })
        .catch(error => {
            console.error('Error loading student files for range:', error);
            alert('Error getting student range from available data');
        });
        return; // Return here as the actual generation will happen in the callback
    }
    
    performBatchGeneration(seatCount, minStudents, maxStudents);
}

// 执行批量生成
function performBatchGeneration(seatCount, minStudents, maxStudents) {
    // Show loading state
    const batchBtn = document.getElementById('batchGenerateBtn');
    const originalText = batchBtn.innerHTML;
    batchBtn.disabled = true;
    batchBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating Batch Plots...';

    fetch('/api/generate_batch_plots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            seat_count: parseInt(seatCount.replace('_seats_simulations', '')),
            min_students: minStudents,
            max_students: maxStudents,
            generate_analysis: true,
            generate_student_plots: true
        })
    })
    .then(response => response.json())
    .then(data => {
        // Reset button
        batchBtn.disabled = false;
        batchBtn.innerHTML = originalText;

        if (data.status === 'success') {
            alert(data.message);
            console.log('Batch generation results:', data.results);
            // 延迟重新加载图像库，确保图像文件已完成写入
            setTimeout(() => {
                loadAvailablePlots();
            }, 3000); // 等待3秒后重新加载，确保图像文件完全写入完成
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        // Reset button
        batchBtn.disabled = false;
        batchBtn.innerHTML = originalText;

        console.error('Error:', error);
        alert('Error occurred: ' + error.message);
    });
}

// 按座位数筛选功能
function filterPlotsBySeatCount() {
    const seatCount = document.getElementById('seatCountForPlot').value;
    
    if (!seatCount) {
        alert('Please select a seat count first');
        return;
    }
    
    const seatNum = parseInt(seatCount.replace('_seats_simulations', ''));
    checkExistingPlotsForSeat(seatNum);
}

// 检查指定座位数的现有图像
function checkExistingPlotsForSeat(seatNum) {
    const plotType = document.getElementById('plotType').value;
    let minStudents = null;
    let maxStudents = null;
    
    if (plotType === 'analysis') {
        const rangeInput = document.getElementById('studentRange').value;
        if (rangeInput && /^\d+-\d+$/.test(rangeInput)) {
            [minStudents, maxStudents] = rangeInput.split('-').map(Number);
        }
    } else {
        // For student plots, we'll check the range from available student files
        const seatFolder = document.getElementById('seatCountForPlot').value;
        fetch(`/api/student_files/${seatFolder}`)
        .then(response => response.json())
        .then(studentFiles => {
            const uniqueStudentCounts = [...new Set(studentFiles.map(file => file.student_count))].sort((a, b) => a - b);
            if (uniqueStudentCounts.length > 0) {
                minStudents = Math.min(...uniqueStudentCounts);
                maxStudents = Math.max(...uniqueStudentCounts);
            }
            performCheckExistingPlots(seatNum, minStudents, maxStudents);
        })
        .catch(error => {
            console.error('Error loading student files for range:', error);
            // If there's an error, just use null for range to get all plots for seat count
            performCheckExistingPlots(seatNum, null, null);
        });
        return;
    }
    
    performCheckExistingPlots(seatNum, minStudents, maxStudents);
}

// 执行检查现有图像
function performCheckExistingPlots(seatNum, minStudents, maxStudents) {
    fetch('/api/check_existing_plots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            seat_count: seatNum,
            min_students: minStudents,
            max_students: maxStudents,
            check_analysis: true,
            check_student_plots: true,
            filter_by_seat_count: false  // We'll handle filtering in the UI
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const results = data.results;
            const summary = data.summary;
            
            // Update the plots gallery to only show matching plots
            // Combine analysis and student plots
            const allFilteredPlots = [...results.analysis_plots, ...results.student_plots];
            updatePlotGalleryWithFilters(allFilteredPlots);
            
            // Show summary info
            const existingPlotsSection = document.getElementById('existingPlotsSection');
            const existingPlotsInfo = document.getElementById('existingPlotsInfo');
            
            let summaryText = `<strong>Existing plots for seat count ${seatNum}:</strong><br>`;
            if (minStudents !== null && maxStudents !== null) {
                summaryText += `In range ${minStudents}-${maxStudents}: `;
            }
            summaryText += `${summary.analysis_count} analysis plots, ${summary.student_count} student plots<br>`;
            summaryText += `<small>Total: ${allFilteredPlots.length} plots found</small>`;
            
            existingPlotsInfo.innerHTML = summaryText;
            document.getElementById('updatePlotBtn').style.display = 'none';
            existingPlotsSection.style.display = 'block';
        } else {
            alert('Error checking existing plots: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error occurred: ' + error.message);
    });
}

// 更新图像库以应用筛选
function updatePlotGalleryWithFilters(filteredPlots) {
    const plotGallery = document.getElementById('plotGallery');
    plotGallery.innerHTML = '';
    
    if (filteredPlots.length === 0) {
        plotGallery.innerHTML = '<div class="col-12"><p>No plots found for the selected seat count.</p></div>';
        return;
    }
    
    filteredPlots.forEach(plot => {
        const plotItem = document.createElement('div');
        plotItem.className = 'col-md-4 col-lg-3 plot-item';
        
        // 确保图像路径正确
        let imagePath = plot.path;
        // 确保路径不包含重复的路径部分
        if (imagePath.startsWith('/')) {
            imagePath = imagePath.substring(1);  // 移除开头的斜杠
        }
        const fullImagePath = `/simulation_data/figures/${imagePath}?t=${new Date().getTime()}`;
        
        plotItem.innerHTML = `
            <div class="card">
                <img src="${fullImagePath}" 
                     alt="${plot.name}" 
                     class="card-img-top plot-thumb"
                     loading="lazy"
                     onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='100%' height='200' viewBox='0 0 200 200'><rect width='100%' height='100%' fill='%23f8f9fa'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='14' fill='%236c757d'>${encodeURIComponent(plot.name)}</text></svg>'; this.classList.add('placeholder-img');">
                <div class="card-body">
                    <h6 class="card-title">${plot.name}</h6>
                    <p class="card-text plot-info">${plot.path}</p>
                </div>
            </div>
        `;
        
        // Add click event to show in modal
        const img = plotItem.querySelector('.plot-thumb');
        img.addEventListener('click', function() {
            showPlotInModal(plot);
        });
        
        plotGallery.appendChild(plotItem);
    });
}

// Show plot in modal
function showPlotInModal(plot) {
    const modalImage = document.getElementById('modalPlotImage');
    // 确保图像路径正确 - 修复路径处理逻辑
    let imagePath = plot.path;
    // 确保路径不包含重复的路径部分
    if (imagePath.startsWith('/')) {
        imagePath = imagePath.substring(1);  // 移除开头的斜杠
    }
    modalImage.src = `/simulation_data/figures/${imagePath}`;
    modalImage.alt = plot.name;
    
    // Show the modal
    const modalElement = new bootstrap.Modal(document.getElementById('plotModal'));
    modalElement.show();
}

// Check for existing plots
function checkExistingPlots() {
    const seatCount = document.getElementById('seatCountForPlot').value;
    const plotType = document.getElementById('plotType').value;
    
    if (!seatCount) {
        alert('Please select a seat count first');
        return;
    }
    
    // Determine the expected plot path based on selection
    let expectedPlotPath;
    const seatNum = seatCount.replace('_seats_simulations', '');
    
    if (plotType === 'analysis') {
        const rangeInput = document.getElementById('studentRange').value;
        if (!rangeInput || !/^\d+-\d+$/.test(rangeInput)) {
            alert('Please enter a valid student range (e.g., 9-19)');
            return;
        }
        const [minStudents, maxStudents] = rangeInput.split('-').map(Number);
        expectedPlotPath = `seats_${seatNum}/analysis(${seatNum}-${minStudents}-${maxStudents}).png`;
    } else {
        const studentCount = document.getElementById('studentCountForPlot').value;
        if (!studentCount) {
            alert('Please select a student count');
            return;
        }
        expectedPlotPath = `seats_${seatNum}/students_${studentCount}.png`;
    }
    
    // Check if plot exists by looking at available plots
    fetch('/api/plots')
    .then(response => response.json())
    .then(plots => {
        const existingPlot = plots.find(plot => plot.path.includes(expectedPlotPath) || plot.path === expectedPlotPath);
        
        const existingPlotsSection = document.getElementById('existingPlotsSection');
        const existingPlotsInfo = document.getElementById('existingPlotsInfo');
        const updatePlotBtn = document.getElementById('updatePlotBtn');
        
        if (existingPlot) {
            existingPlotsInfo.innerHTML = `
                <strong>Existing plot found:</strong> ${existingPlot.name}<br>
                <small>Path: ${existingPlot.path}</small>
            `;
            updatePlotBtn.style.display = 'inline-block';
        } else {
            existingPlotsInfo.innerHTML = `
                <strong>No existing plot found</strong> for the selected parameters.<br>
                A new plot will be generated.
            `;
            updatePlotBtn.style.display = 'none';
        }
        
        // Store the expected path for later use
        window.expectedPlotPath = expectedPlotPath;
        existingPlotsSection.style.display = 'block';
    })
    .catch(error => {
        console.error('Error checking existing plots:', error);
        document.getElementById('existingPlotsInfo').innerHTML = `Error checking existing plots: ${error.message}`;
        document.getElementById('existingPlotsSection').style.display = 'block';
    });
}

// Generate plots from selected parameters
function generatePlots(forceUpdate = false) {
    const seatCount = document.getElementById('seatCountForPlot').value;
    const plotType = document.getElementById('plotType').value;
    
    if (!seatCount) {
        alert('Please select a seat count');
        return;
    }
    
    if (plotType === 'student') {
        const studentCount = document.getElementById('studentCountForPlot').value;
        if (!studentCount) {
            alert('Please select a student count');
            return;
        }
        
        // For student plots, we generate using save_figure with simulation_number=1
        const seatNum = parseInt(seatCount.replace('_seats_simulations', ''));
        
        // Show loading state
        document.getElementById('generatePlotBtn').disabled = true;
        document.getElementById('generatePlotBtn').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
        
        // Call backend API to generate plots
        fetch('/api/generate_plots', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                seat_count: seatNum,
                student_count: parseInt(studentCount),
                plot_type: 'student'
            })
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            document.getElementById('generatePlotBtn').disabled = false;
            document.getElementById('generatePlotBtn').textContent = 'Generate Plots';
            
            if (data.status === 'success') {
                alert(data.message);
                console.log('Generated plot path:', data.expected_path);
                // 延迟重新加载图像库，确保图像文件已完成写入
                setTimeout(() => {
                    loadAvailablePlots();
                }, 1000); // 等待1秒后重新加载，确保图像文件完全写入完成
                
                // Close the existing plots section if open
                document.getElementById('existingPlotsSection').style.display = 'none';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            // Reset button
            document.getElementById('generatePlotBtn').disabled = false;
            document.getElementById('generatePlotBtn').textContent = 'Generate Plots';
            
            console.error('Error:', error);
            alert('Error occurred: ' + error.message);
        });
    } else if (plotType === 'analysis') {
        const studentRange = document.getElementById('studentRange').value;
        if (!studentRange || !/^\d+-\d+$/.test(studentRange)) {
            alert('Please enter a valid student range (e.g., 9-19)');
            return;
        }
        
        const seatNum = parseInt(seatCount.replace('_seats_simulations', ''));
        const [minStudents, maxStudents] = studentRange.split('-').map(Number);
        
        // Show loading state
        document.getElementById('generatePlotBtn').disabled = true;
        document.getElementById('generatePlotBtn').innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating (this may take a while for analysis plots)...';
        
        // Call backend API to generate analysis plots
        fetch('/api/generate_plots', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                seat_count: seatNum,
                min_students: minStudents,
                max_students: maxStudents,
                plot_type: 'analysis'
            })
        })
        .then(response => response.json())
        .then(data => {
            // Reset button
            document.getElementById('generatePlotBtn').disabled = false;
            document.getElementById('generatePlotBtn').textContent = 'Generate Plots';
            
            if (data.status === 'success') {
                alert(data.message);
                console.log('Generated plot path:', data.expected_path);
                // 延迟重新加载图像库，确保图像文件已完成写入
                setTimeout(() => {
                    loadAvailablePlots();
                }, 2000); // 等待2秒后重新加载，确保图像文件完全写入完成
                
                // Close the existing plots section if open
                document.getElementById('existingPlotsSection').style.display = 'none';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            // Reset button
            document.getElementById('generatePlotBtn').disabled = false;
            document.getElementById('generatePlotBtn').textContent = 'Generate Plots';
            
            console.error('Error:', error);
            alert('Error occurred: ' + error.message);
        });
    }
}