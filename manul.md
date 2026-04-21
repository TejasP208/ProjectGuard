# Starting the Frontend Database Server:
- **First**, `cd` into the project file (open in terminal)
- **Run**: `python3 -m http.server 8080`
- **Student Portal**: Open `http://localhost:8080/Frontend/auth.html` in your browser
- **Mentor Portal**: Open `http://localhost:8080/Mentor%20Portal/auth.html` in your browser

# Starting the FastAPI Backend:
Open a **new** terminal (keep the frontend web server running in the other one!) and `cd` into the project file again:
- **Run one of these**:
  - `python3 main.py`
  - OR `python3 -m uvicorn main:app --reload` (this version auto-restarts when you edit the code!)
- **Backend API**: Open `http://127.0.0.1:8000/api/projects` to test the JSON data.