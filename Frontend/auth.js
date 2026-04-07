document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const authTitle = document.getElementById('auth-title');
    const authSubtitle = document.getElementById('auth-subtitle');
    const showSignup = document.getElementById('show-signup');
    const showLogin = document.getElementById('show-login');

    // Switch to Signup
    showSignup.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
        authTitle.textContent = 'Create Account';
        authSubtitle.textContent = 'Register your group of 4 students';
    });

    // Switch to Login
    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        signupForm.style.display = 'none';
        loginForm.style.display = 'block';
        authTitle.textContent = 'Welcome Back';
        authSubtitle.textContent = 'Please Enter your details to continue';
    });

    // Handle Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = loginForm.querySelector('button');
        const span = btn.querySelector('span');
        const originalText = span.textContent;
        
        span.textContent = 'Logging in...';
        btn.disabled = true;

        const teamName = document.getElementById('login-roll').value;
        const password = document.getElementById('login-pass').value;

        try {
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    team_name: teamName,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store login info in localStorage
                localStorage.setItem('loggedInTeam', teamName);
                window.location.href = 'index.html';
            } else {
                alert(data.detail || 'Login failed');
                span.textContent = originalText;
                btn.disabled = false;
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Network error. Please try again.');
            span.textContent = originalText;
            btn.disabled = false;
        }
    });

    // Handle Signup
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = signupForm.querySelector('button');
        const span = btn.querySelector('span');
        
        span.textContent = 'Creating account...';
        btn.disabled = true;

        const formData = {
            roll1: document.getElementById('roll-1').value,
            roll2: document.getElementById('roll-2').value,
            roll3: document.getElementById('roll-3').value,
            roll4: document.getElementById('roll-4').value,
            team_name: document.getElementById('team-name').value,
            year: document.getElementById('year').value,
            mentor_name: document.getElementById('mentor-name').value,
            password: document.getElementById('signup-pass').value
        };

        try {
            const response = await fetch('http://localhost:8000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                alert('Account created successfully! You can now login.');
                showLogin.click();
            } else {
                alert(data.detail || 'Signup failed');
            }
        } catch (error) {
            console.error('Signup error:', error);
            alert('Network error. Please try again.');
        }

        span.textContent = 'Create Account';
        btn.disabled = false;
    });
});
