document.addEventListener('DOMContentLoaded', () => {
    // Input Variables
    window.projectDataStore = {
        title: "",
        description: ""
    };

    // Elements
    const titleInput = document.getElementById('project-title');
    const descInput = document.getElementById('project-desc');
    const btnSubmit = document.getElementById('btn-submit');
    const form = document.getElementById('submission-form');

    // Store inputs dynamically when typing
    if (titleInput) {
        titleInput.addEventListener('input', (e) => {
            window.projectDataStore.title = e.target.value;
            console.log("Project Title Updated:", window.projectDataStore.title);
        });
    }

    if (descInput) {
        descInput.addEventListener('input', (e) => {
            window.projectDataStore.description = e.target.value;
            console.log("Project Description Updated:", window.projectDataStore.description);
        });
    }

    // Form Submission for standard form
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            btnSubmit.innerHTML = '<i class="ph ph-spinner-gap"></i> Processing...';
            
            setTimeout(() => {
                alert(`Submission successful!\nTitle: ${window.projectDataStore.title}`);
                btnSubmit.innerHTML = '<i class="ph ph-check"></i> Submitted';
                btnSubmit.style.background = 'var(--status-verified)';
            }, 1000);
        });
    }

    // Acceptance Form Logic
    const acceptanceForm = document.getElementById('acceptance-form');
    if (acceptanceForm) {
        acceptanceForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            btnSubmit.innerHTML = '<i class="ph ph-spinner-gap"></i> Checking AI Models...';
            btnSubmit.disabled = true;

            try {
                const response = await fetch('http://127.0.0.1:8000/api/check_project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        title: window.projectDataStore.title,
                        description: window.projectDataStore.description
                    })
                });
                
                const result = await response.json();

                if (result.exists) {
                    alert(`REJECTED: A similar project already exists.\nMatched with: ${result.best_match.name}`);
                    btnSubmit.innerHTML = '<i class="ph ph-warning-circle"></i> Rejected';
                    btnSubmit.style.background = 'var(--status-pending)'; // Yellowish or red depending on CSS
                } else {
                    alert("ACCEPTED: No matching project found. You are good to go!");
                    btnSubmit.innerHTML = '<i class="ph ph-check-circle"></i> Accepted';
                    btnSubmit.style.background = 'var(--status-verified)';
                }
            } catch (error) {
                console.error("Error checking project:", error);
                alert("Failed to connect to the server. Make sure the backend API is running.");
                btnSubmit.innerHTML = 'Error';
            } finally {
                btnSubmit.disabled = false;
            }
        });
    }
});
