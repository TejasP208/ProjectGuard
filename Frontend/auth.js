import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyBGXgPMyXLGZAXYq0aLFvD1EIHpNlDeM0A",
    authDomain: "project-guard-19f21.firebaseapp.com",
    projectId: "project-guard-19f21",
    storageBucket: "project-guard-19f21.firebasestorage.app",
    messagingSenderId: "334400351259",
    appId: "1:334400351259:web:9460acdd8bbc5844585cbe",
    measurementId: "G-WEMJ0J7C13"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Helper to format ID to email
const formatUsernameToEmail = (username) => {
    if (username.includes('@')) return username;
    return `${username}@projectguard.local`;
};

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
        
        const username = document.getElementById('login-roll').value.trim();
        const password = document.getElementById('login-pass').value;

        span.textContent = 'Logging in...';
        btn.disabled = true;

        try {
            const email = formatUsernameToEmail(username);
            await signInWithEmailAndPassword(auth, email, password);
            
            // Allow login without checking Firestore roles for now
            window.location.href = 'index.html';
        } catch (error) {
            console.error(error.code, error.message);
            if(error.code === 'auth/invalid-credential') {
                alert('Invalid username or password.');
            } else {
                alert('Login failed: ' + error.message);
            }
            span.textContent = originalText;
            btn.disabled = false;
        }
    });

    // Handle Signup 
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = signupForm.querySelector('button');
        const span = btn.querySelector('span');
        const originalText = span.textContent;

        const signupId = document.getElementById('signup-id').value.trim();
        const password = document.getElementById('signup-pass').value;
        
        span.textContent = 'Creating account...';
        btn.disabled = true;

        try {
            const email = formatUsernameToEmail(signupId);
            await createUserWithEmailAndPassword(auth, email, password);
            
            alert('Account created successfully! You can now login.');
            document.getElementById('login-roll').value = signupId;
            showLogin.click();
            span.textContent = originalText;
            btn.disabled = false;
            signupForm.reset();
        } catch (error) {
            console.error(error.code, error.message);
            if(error.code === 'auth/email-already-in-use') {
                alert('This Username or PRN is already registered.');
            } else if (error.code === 'auth/weak-password') {
                alert('Password should be at least 6 characters.');
            } else {
                alert('Signup failed: ' + error.message);
            }
            span.textContent = originalText;
            btn.disabled = false;
        }
    });
});
