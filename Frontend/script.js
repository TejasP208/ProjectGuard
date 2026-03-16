document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadProgressArea = document.getElementById('upload-progress-area');
    const fileNameDisplay = document.getElementById('file-name-display');
    const removeFileBtn = document.getElementById('remove-file');
    const progressBar = document.getElementById('upload-progress-bar');
    const uploadPercentage = document.getElementById('upload-percentage');
    const uploadStatusText = document.getElementById('upload-status-text');
    
    // Buttons
    const btnSubmit = document.getElementById('btn-submit');
    const btnCheck = document.getElementById('btn-check');

    // Evaluation
    const evalPanel = document.getElementById('evaluation-panel');
    const chipPending = document.getElementById('chip-pending');
    const chipChecking = document.getElementById('chip-checking');
    const chipVerified = document.getElementById('chip-verified');
    const scoreContainer = document.getElementById('score-container');
    const scoreValue = document.getElementById('score-value');
    
    // File state
    let currentFile = null;

    // --- Drag and Drop Logic --- //
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drop zone
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', (e) => {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    });

    // Click to upload
    dropZone.addEventListener('click', () => {
        if(!currentFile) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            // Check file type / validation here if needed
            currentFile = files[0];
            startUploadSimulation(currentFile.name);
        }
    }

    // --- Upload Simulation Logic --- //
    function startUploadSimulation(fileName) {
        // Hide dropzone interior, show progress
        dropZone.style.display = 'none';
        uploadProgressArea.style.display = 'block';
        evalPanel.style.display = 'block'; // Show eval panel as Pending
        
        fileNameDisplay.textContent = fileName;
        progressBar.style.width = '0%';
        uploadPercentage.textContent = '0%';
        uploadStatusText.textContent = 'Uploading...';
        
        // Reset eval state
        resetEvalState();
        
        // Disable buttons during upload
        btnSubmit.disabled = true;
        btnCheck.disabled = true;

        let progress = 0;
        const uploadInterval = setInterval(() => {
            progress += Math.random() * 15; // Random interval increase
            if (progress >= 100) {
                progress = 100;
                clearInterval(uploadInterval);
                finishUpload();
            }
            progressBar.style.width = progress + '%';
            uploadPercentage.textContent = Math.round(progress) + '%';
        }, 300);
    }

    function finishUpload() {
        uploadStatusText.textContent = 'Upload Complete';
        uploadStatusText.style.color = 'var(--status-verified)';
        progressBar.style.background = 'var(--status-verified)';
        
        // Enable buttons
        btnSubmit.disabled = false;
        btnCheck.disabled = false;
    }

    // --- Remove File Logic --- //
    removeFileBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        dropZone.style.display = 'block';
        uploadProgressArea.style.display = 'none';
        evalPanel.style.display = 'none';
        
        btnSubmit.disabled = true;
        btnCheck.disabled = true;
        progressBar.style.background = 'linear-gradient(90deg, var(--primary), var(--secondary))';
        uploadStatusText.style.color = 'var(--text-muted)';
    });


    // --- Anti-Gravity Checking Simulation --- //
    btnCheck.addEventListener('click', () => {
        if(!currentFile) return;

        // Ui State Updates
        btnCheck.disabled = true;
        btnCheck.innerHTML = '<i class="ph-fill ph-spinner-gap"></i> Checking...';
        btnSubmit.disabled = true;
        
        chipPending.style.display = 'none';
        chipChecking.style.display = 'inline-flex';
        
        // Simulate checking process
        setTimeout(() => {
            finishChecking();
        }, 2500);
    });

    function finishChecking() {
        btnCheck.innerHTML = '<i class="ph-fill ph-check-circle"></i> Checked';
        btnSubmit.disabled = false;

        chipChecking.style.display = 'none';
        chipVerified.style.display = 'inline-flex';

        // Show Score
        scoreContainer.style.display = 'flex';
        
        // Add subtle animation
        scoreContainer.style.animation = 'fadeIn 0.5s ease frontwards';
    }

    function resetEvalState() {
        chipPending.style.display = 'inline-flex';
        chipChecking.style.display = 'none';
        chipVerified.style.display = 'none';
        scoreContainer.style.display = 'none';
        
        btnCheck.innerHTML = '<i class="ph-fill ph-shield-check"></i> Check  Plagiarism';
    }

    // Form Submission
    const form = document.getElementById('submission-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        btnSubmit.innerHTML = '<i class="ph ph-spinner-gap"></i> Submitting...';
        
        setTimeout(() => {
            alert('Project submitted successfully! Your instructor will review it soon.');
            btnSubmit.innerHTML = '<i class="ph ph-check"></i> Submitted';
            btnSubmit.style.background = 'var(--status-verified)';
        }, 1500);
    });
});
