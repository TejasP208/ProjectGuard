document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const loggedInTeam = localStorage.getItem('loggedInTeam');
    if (!loggedInTeam) {
        window.location.href = 'auth.html';
        return;
    }

    // Update user profile with team name
    const userNameElement = document.querySelector('.user-name');
    if (userNameElement) {
        userNameElement.textContent = loggedInTeam;
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('loggedInTeam');
            window.location.href = 'auth.html';
        });
    }

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

    // --- Navigation & View Switching --- //
    const navItems = {
        'nav-dashboard': 'view-dashboard',
        'nav-find': 'view-find',
        'nav-submit': 'view-submit',
        'nav-plagiarism': 'view-plagiarism',
        'nav-settings': 'view-settings'
    };

    function switchView(targetNavId) {
        // Update active nav class
        document.querySelectorAll('.sidebar-nav .nav-item').forEach(nav => {
            nav.classList.remove('active');
        });
        document.getElementById(targetNavId).classList.add('active');

        // Hide all views, show target view
        document.querySelectorAll('.content-view').forEach(view => {
            view.classList.add('hidden');
        });
        document.getElementById(navItems[targetNavId]).classList.remove('hidden');
    }

    // Attach click listeners to nav items
    Object.keys(navItems).forEach(navId => {
        const navEl = document.getElementById(navId);
        if (navEl) {
            navEl.addEventListener('click', (e) => {
                e.preventDefault();
                switchView(navId);
            });
        }
    });

    // Initialize default view based on active nav item
    const activeNav = document.querySelector('.sidebar-nav .nav-item.active');
    if (activeNav) {
        switchView(activeNav.id);
    }

    // --- Axiom AI Integration --- //
    function setupAxiomAI(inputId, btnId, chatBoxId) {
        const input = document.getElementById(inputId);
        const btn = document.getElementById(btnId);
        const chatBox = document.getElementById(chatBoxId);

        if (!input || !btn || !chatBox) return;

        // Premium AI Responses
        const responses = [
            "Analyzing your request based on your recent project submissions...",
            "I found 3 relevant drafts in your history. Here is a quick summary for you.",
            "That's an excellent question! Based on my semantic search of your knowledge base, here's what you need to know.",
            "I'm cross-referencing your project guidelines with your current draft. Please allow me a moment.",
            "Your previous 'AI Algorithms' assignment had a perfectly aligned methodology. I suggest reviewing Section 3."
        ];

        function sendMessage() {
            const text = input.value.trim();
            if(!text) return;

            // Add user message with premium styling
            const userWrapper = document.createElement('div');
            userWrapper.className = 'message-wrapper user-wrapper';
            
            const userAvatar = document.createElement('div');
            userAvatar.className = 'message-avatar';
            userAvatar.innerHTML = '<i class="ph-fill ph-user"></i>';
            
            const userMsg = document.createElement('div');
            userMsg.className = 'premium-glass-bubble';
            userMsg.textContent = text;
            
            userWrapper.appendChild(userAvatar);
            userWrapper.appendChild(userMsg);
            chatBox.appendChild(userWrapper);
            
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Disable Send Button
            const originalBtnHtml = btn.innerHTML;
            btn.innerHTML = '<i class="ph ph-spinner-gap ph-spin"></i>';
            btn.disabled = true;

            // Show AI Typing Indicator
            const aiWrapper = document.createElement('div');
            aiWrapper.className = 'message-wrapper ai-wrapper';
            
            const aiAvatar = document.createElement('div');
            aiAvatar.className = 'message-avatar';
            aiAvatar.innerHTML = '<i class="ph-fill ph-terminal-window"></i>';
            
            const typingMsg = document.createElement('div');
            typingMsg.className = 'typing-indicator';
            typingMsg.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
            
            aiWrapper.appendChild(aiAvatar);
            aiWrapper.appendChild(typingMsg);
            chatBox.appendChild(aiWrapper);
            chatBox.scrollTop = chatBox.scrollHeight;

            // Simulate Thinking Delay, then Type out response
            setTimeout(() => {
                // Pick a random smart response
                const responseText = responses[Math.floor(Math.random() * responses.length)];
                
                // Replace typing indicator with empty glass bubble
                aiWrapper.removeChild(typingMsg);
                const finalMsg = document.createElement('div');
                finalMsg.className = 'ai-message premium-glass-bubble';
                finalMsg.innerHTML = `<p><strong>Axiom AI:</strong> <span class="typing-text"></span></p>`;
                aiWrapper.appendChild(finalMsg);
                
                const textSpan = finalMsg.querySelector('.typing-text');
                let charIndex = 0;
                
                // Typing effect
                const typeInterval = setInterval(() => {
                    if (charIndex < responseText.length) {
                        textSpan.textContent += responseText.charAt(charIndex);
                        charIndex++;
                        chatBox.scrollTop = chatBox.scrollHeight;
                    } else {
                        clearInterval(typeInterval);
                        btn.innerHTML = originalBtnHtml;
                        btn.disabled = false;
                        
                        // Give input focus back
                        input.focus();
                    }
                }, 20); // 20ms per character for fast reading
                
            }, 1200); // 1.2s thinking time
        }

        btn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') sendMessage();
        });
    }

    // setupAxiomAI('dashboard-chat-input', 'dashboard-send-btn', 'dashboard-chat-box'); // Removed per layout changes
    setupAxiomAI('find-chat-input', 'find-send-btn', 'find-chat-box');
});
const input = document.getElementById("find-chat-input");
const sendBtn = document.getElementById("find-send-btn");
const chatBox = document.getElementById("find-chat-box");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    //  User message
    chatBox.innerHTML += `
        <div class="message-wrapper user-wrapper">
            <div class="user-message">${message}</div>
        </div>
    `;

    input.value = "";

    //  Create empty AI message container
    const aiWrapper = document.createElement("div");
    aiWrapper.className = "message-wrapper ai-wrapper";

    const aiMessage = document.createElement("div");
    aiMessage.className = "ai-message";

    aiWrapper.appendChild(aiMessage);
    chatBox.appendChild(aiWrapper);

    try {
        const res = await fetch(`http://127.0.0.1:8000/chat-stream?prompt=${encodeURIComponent(message)}`);

        const reader = res.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            //  Append streaming text
            aiMessage.textContent += decoder.decode(value);

            // Auto scroll
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (err) {
        aiMessage.textContent = "Error connecting to server";
        console.error(err);
    }
}
// ==================== AUTH ====================

async function signup() {
    const data = {
        roll1: document.getElementById("roll1").value,
        roll2: document.getElementById("roll2").value,
        roll3: document.getElementById("roll3").value,
        roll4: document.getElementById("roll4").value,
        team_name: document.getElementById("team-name").value,
        year: document.getElementById("year").value,
        mentor_name: document.getElementById("mentor").value,
        password: document.getElementById("password").value
    };

    const res = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);
}


// ==================== LOGIN ====================

async function login() {
    const data = {
        team_name: document.getElementById("team-name").value,
        password: document.getElementById("password").value
    };

    const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    async function login() {
    const data = {
        team_name: document.getElementById("team-name").value,
        password: document.getElementById("password").value
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        // ✅ Proper validation
        if (res.status === 200 && result.message === "Login successful") {
            alert("Login successful");

            // store token later if added
            // localStorage.setItem("token", result.token);

            window.location.href = "dashboard.html";  // redirect
        } else {
            alert(result.error || "Login failed");
        }

    } catch (err) {
        console.error(err);
        alert("Server error");
    }
}       

        else {
        alert("Invalid credentials");
    }
}