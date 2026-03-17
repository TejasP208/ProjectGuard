document.addEventListener('DOMContentLoaded', () => {
    // Navigation Items
    const navDashboard = document.getElementById('nav-dashboard');
    const navProjectList = document.getElementById('nav-project-list');
    const navStudentList = document.getElementById('nav-student-list');
    
    // Content Areas
    const mainTitle = document.getElementById('main-title');
    const mainSubtitle = document.getElementById('main-subtitle');
    const contentContainer = document.getElementById('content-container');

    const navItems = [navDashboard, navProjectList, navStudentList];

    function setActiveNav(activeItem) {
        navItems.forEach(item => {
            if (item) item.classList.remove('active');
        });
        if (activeItem) activeItem.classList.add('active');
    }

    // Dashboard View
    if (navDashboard) {
        navDashboard.addEventListener('click', (e) => {
            e.preventDefault();
            setActiveNav(navDashboard);
            mainTitle.textContent = 'Mentor Dashboard';
            mainSubtitle.textContent = 'Overview of your assigned student groups';
            
            contentContainer.innerHTML = `
                <div class="card glass-card" style="min-height: 400px; display: flex; align-items: center; justify-content: center; flex-direction: column; text-align: center; color: var(--text-muted);">
                    <i class="ph ph-squares-four" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <h2>Dashboard Empty</h2>
                    <p>Metrics and updates will appear here.</p>
                </div>
            `;
        });
    }

    // Mock Project Data
    const mockProjects = [
        { id: 1, title: 'AI Based Plagiarism Checker', team: 'Innovators', year: 'Fourth Year', groupNo: '18', status: 'verified', score: '12%' },
        { id: 2, title: 'Smart Campus Navigation', team: 'Navigators', year: 'Third Year', groupNo: '12', status: 'pending', score: '--' },
        { id: 3, title: 'Library Management System', team: 'CodeCrafters', year: 'Second Year', groupNo: '05', status: 'checking', score: '--' },
        { id: 4, title: 'IoT Weather Station', team: 'SensorSquad', year: 'Third Year', groupNo: '09', status: 'verified', score: '5%' },
        { id: 5, title: 'Blockchain Voting App', team: 'CyberNet', year: 'Fourth Year', groupNo: '24', status: 'pending', score: '--' }
    ];

    // Helper to render the Project List UI
    function renderProjectListUI() {
        mainTitle.textContent = 'Project List';
        mainSubtitle.textContent = 'View submitted projects from your groups';
        
        contentContainer.innerHTML = `
            <div class="filter-container">
                <span class="filter-label"><i class="ph ph-funnel"></i> Filter by Year:</span>
                <div class="checkbox-group" id="year-filters">
                    <label class="checkbox-item">
                        <input type="checkbox" value="Second Year"> Second Year
                    </label>
                    <label class="checkbox-item">
                        <input type="checkbox" value="Third Year"> Third Year
                    </label>
                    <label class="checkbox-item">
                        <input type="checkbox" value="Fourth Year"> Fourth Year
                    </label>
                </div>
            </div>
            <div class="project-grid" id="project-grid-container">
                <!-- Projects will be injected here -->
            </div>
        `;

        const filterCheckboxes = document.querySelectorAll('#year-filters input[type="checkbox"]');
        const gridContainer = document.getElementById('project-grid-container');

        // Function to render projects based on selected filters
        function updateProjectDisplay() {
            // Get selected years
            const selectedYears = Array.from(filterCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            
            // Filter logic: If nothing selected, show all. Else show matching years.
            let filteredProjects = mockProjects;
            if (selectedYears.length > 0) {
                filteredProjects = mockProjects.filter(p => selectedYears.includes(p.year));
            }

            // Render
            if (filteredProjects.length === 0) {
                gridContainer.innerHTML = `
                    <div class="empty-state">
                        <i class="ph ph-folder-dashed"></i>
                        <h3>No Projects Found</h3>
                        <p>No projects match your current filter selection.</p>
                    </div>
                `;
                return;
            }

            let html = '';
            filteredProjects.forEach(p => {
                // Determine chip style
                let chipClass = 'pending';
                let chipIcon = 'ph-clock';
                let chipText = 'Pending';
                
                if(p.status === 'checking') {
                    chipClass = 'checking';
                    chipIcon = 'ph-spinner-gap';
                    chipText = 'Checking';
                } else if (p.status === 'verified') {
                    chipClass = 'verified';
                    chipIcon = 'ph-check-circle';
                    chipText = 'Verified';
                }

                html += `
                    <div class="project-card">
                        <div class="project-info">
                            <h3 class="project-title">${p.title}</h3>
                            <div class="project-meta">
                                <span><i class="ph ph-users"></i> ${p.team}</span>
                                <span><i class="ph ph-calendar-blank"></i> ${p.year}</span>
                                <span><i class="ph ph-hash"></i> Group ${p.groupNo}</span>
                            </div>
                        </div>
                        <div class="project-actions">
                            <span class="chip ${chipClass}"><i class="ph ${chipIcon}"></i> ${chipText}</span>
                            <button class="icon-btn glass-btn" title="View Details">
                                <i class="ph ph-caret-right"></i>
                            </button>
                        </div>
                    </div>
                `;
            });
            gridContainer.innerHTML = html;
        }

        // Attach listeners
        filterCheckboxes.forEach(cb => {
            cb.addEventListener('change', updateProjectDisplay);
        });

        // Initial render
        updateProjectDisplay();
    }

    // Project List View
    if (navProjectList) {
        navProjectList.addEventListener('click', (e) => {
            e.preventDefault();
            setActiveNav(navProjectList);
            renderProjectListUI();
        });
    }

    // Student List View
    if (navStudentList) {
        navStudentList.addEventListener('click', (e) => {
            e.preventDefault();
            setActiveNav(navStudentList);
            mainTitle.textContent = 'Student List';
            mainSubtitle.textContent = 'Manage student groups under your guidance';
            
            contentContainer.innerHTML = `
                <div class="card glass-card" style="min-height: 400px; display: flex; align-items: center; justify-content: center; flex-direction: column; text-align: center; color: var(--text-muted);">
                    <i class="ph ph-users" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                    <h2>Student List Empty</h2>
                    <p>Student groups under your supervision will be listed here.</p>
                </div>
            `;
        });
    }
});
