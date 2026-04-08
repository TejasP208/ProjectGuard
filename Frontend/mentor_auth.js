import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-firestore.js";
import { firebaseConfig } from "../env.js";

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Helper to format ID to email
const formatUsernameToEmail = (username) => {
    if (username.includes('@')) return username;
    return `${username}@projectguard.local`;
};


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
        authSubtitle.textContent = 'Enter your details to register';
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
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            // Check Firestore roles
            const docRef = doc(db, "users", user.uid);
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                const userData = docSnap.data();
                if (userData.role === "mentor") {
                    window.location.href = 'mentor_index.html';
                } else {
                    await signOut(auth);
                    alert("Access Denied: Please use the Student Portal.");
                    span.textContent = originalText;
                    btn.disabled = false;
                }
            } else {
                await signOut(auth);
                alert("User role not found. Please contact support.");
                span.textContent = originalText;
                btn.disabled = false;
            }
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
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;

            await setDoc(doc(db, "users", user.uid), {
                prn: signupId,
                role: "mentor"
            });
            
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