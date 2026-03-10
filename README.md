# HRMS Lite

Simple full‑stack Human Resource Management System to manage employees and daily attendance.

Backend is built with **FastAPI + SQLite**, organised into a small `app` package (config, database, schemas, services, routers).  
The frontend is a **single HTML page with vanilla JavaScript** that talks to the REST API.

---

## Features

- **Employee Management**
  - Add employee with `employee_id`, full name, email, department
  - List all employees
  - Delete employee (also removes their attendance)
- **Attendance Management**
  - Mark attendance for an employee for a given day (`Present` / `Absent`)
  - View attendance history per employee
  - View summary: total present and absent days per employee
- **Good UX**
  - Clean, simple dashboard‑style layout
  - Loading, empty, and error states

---

## Tech Stack

- **Backend**: Python, FastAPI, SQLite (via `sqlite3`)
- **Frontend**: HTML, CSS, vanilla JavaScript (`fetch` API)
- **Deployment (suggested)**:
  - Frontend: Netlify / Vercel
  - Backend: Render / Railway (Docker or Python web service)

---

## Running the project locally

### 1. Create and activate a virtual environment (recommended)

```bash
cd /path/to/project
python -m venv venv
source venv/bin/activate  # on macOS / Linux
# venv\Scripts\activate   # on Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment (optional but recommended)

Copy the example file and adjust values if you need:

```bash
cp .env.example .env
```

Defaults:

- `DB_PATH=hrms.db` – SQLite database file in the project root
- `CORS_ORIGINS=*` – allow all origins (for local development only)

### 4. Run the backend (FastAPI)

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` (or another port if you set it).

Useful endpoints:

- `GET /health` – health check
- `GET /employees` – list employees
- `POST /employees` – create employee
- `DELETE /employees/{employee_id}` – delete employee
- `POST /employees/{employee_id}/attendance` – mark attendance
- `GET /employees/{employee_id}/attendance` – view attendance
- `GET /employees/{employee_id}/attendance/summary` – attendance summary

You can also open the automatic API docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Open the frontend

Open the file `frontend/index.html` directly in your browser, or serve the `frontend` folder using any simple static server.

By default the page expects the backend at:

```js
const API_BASE_URL = "http://localhost:8000";
```

If you deploy the backend, change this URL in `frontend/index.html` to your live backend URL.

---

## Deployment Guide (example)

### Backend (Render example)

1. Push this project to GitHub.
2. Create a new **Web Service** on Render.
3. Select your repo and set:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add environment variable if needed (optional). SQLite DB file (`hrms.db`) will be created automatically.
5. After deployment, note your live backend URL, for example:
   - `https://your-hrms-backend.onrender.com`

### Frontend (Netlify example)

1. In Netlify, create a **New site from Git** and choose the same repository or another repo containing only the `frontend` folder.
2. If using the same repo:
   - Build command: leave empty (static site).
   - Publish directory: `frontend`
3. After deployment, you will get a public URL, like:
   - `https://your-hrms-frontend.netlify.app`
4. In `frontend/index.html`, set:

```js
const API_BASE_URL = "https://your-hrms-backend.onrender.com";
```

and re‑deploy the frontend if needed.

---

## Assumptions & Limitations

- Only a single admin user is assumed; **no authentication** is implemented.
- SQLite is used for simplicity; for a bigger system you would use PostgreSQL/MySQL.
- No pagination for lists (employees/attendance) to keep the code very simple.
- Basic email format validation is handled by FastAPI / Pydantic (`EmailStr`).
- CORS origins are taken from `CORS_ORIGINS` in `.env`; in production, set this to your actual frontend domain instead of `*`.


