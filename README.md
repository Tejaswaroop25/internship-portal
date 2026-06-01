# InternMatch: AI Internship Matching & Application Portal

InternMatch is a premium, fully-featured Flask application designed to connect students with optimal internship positions using a customized, skill-based AI recommendation engine. It includes gorgeous, responsive Glassmorphic Dark-themed templates, dynamic styling, and customized dashboards for Students, Companies, and Administrators.

---

## 🚀 Step-by-Step Running Guide

Follow these simple steps inside your terminal to activate the virtual environment and start the development server.

### 1. Open PowerShell or Command Prompt
Navigate to your project folder:
```bash
cd c:\Users\nanit\OneDrive\Desktop\@D46\M\internship-portal
```

### 2. Activate the Virtual Environment

- **On Windows (PowerShell)**:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
- **On Windows (Command Prompt - CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

### 3. Run the Development Server
Execute the Flask server script:
```bash
python backend/app.py
```

The terminal will display:
```text
Seeding initial mock data...
Mock data seeded successfully!
 * Serving Flask app 'backend.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser!

---

## 🔑 Pre-Seeded Test Credentials

The database is automatically created and seeded with mock accounts on first startup so you can test all features immediately!

### 1. Student Accounts (Evaluate matching & recommendations)
- **John Doe** (Backend Python Focus):
  - **Email**: `john@student.edu`
  - **Password**: `student123`
  - **Skills**: `Python, Flask, SQLite, HTML, CSS`
- **Alice Smith** (Frontend UI/UX Focus):
  - **Email**: `alice@student.edu`
  - **Password**: `student123`
  - **Skills**: `Figma, UI/UX, CSS, JavaScript, React`

### 2. Company Accounts (Publish postings & screen applications)
- **TechCorp Inc.** (Backend & Automation recruiter):
  - **Email**: `jobs@techcorp.com`
  - **Password**: `company123`
- **DesignLab Studio** (Digital UX & Design agency):
  - **Email**: `careers@designlab.co`
  - **Password**: `company123`

### 3. Platform Admin Account (View registered users directory)
- **Super Administrator**:
  - **Email**: `admin@portal.com`
  - **Password**: `admin123`

---

## 🛠️ Project Architecture

```text
internship-portal/
├── backend/
│   ├── database/
│   │   └── db.sqlite             <-- Auto-created SQLite DB
│   ├── models/
│   │   ├── __init__.py           <-- Initializes SQLAlchemy DB object
│   │   ├── user.py               <-- Accounts & Profile (Student / Company details)
│   │   ├── internship.py         <-- Job posts created by companies
│   │   └── application.py        <-- Student submissions
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py               <-- Register, Login, Dashboards, Profile edits
│   │   ├── internships.py        <-- Jobs CRUD (search, create, modify)
│   │   ├── applications.py       <-- Submissions & Status screeners
│   │   └── recommendations.py    <-- AI Matching view
│   ├── services/
│   │   └── recommendation_service.py <-- Skill matching calculation service
│   ├── app.py                    <-- App factory & Mock Seeding pipeline
│   ├── config.py                 <-- Configures SQLite path & Secret Keys
│   └── requirements.txt          <-- Package dependencies list
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         <-- Modern Glassmorphism Styling system
│   │   └── js/
│   │       └── app.js            <-- Skill tags manager & fadeout alerts
│   └── templates/
│       ├── base.html             <-- Global header, footer, & Toast broadcast
│       ├── login.html            <-- Glass card credential auth
│       ├── register.html         <-- Multi-role responsive signups
│       ├── student_dashboard.html<-- Applied trackers & Match list
│       ├── company_dashboard.html<-- Recruiter listing controls & Candidates
│       ├── internship_listing.html<-- Interactive jobs browsing & keywords
│       ├── internship_detail.html<-- Detailed descriptions & gauge meters
│       ├── create_internship.html<-- Publish job form
│       ├── edit_internship.html  <-- Prefilled update form
│       ├── apply.html            <-- Cover letter pitches
│       ├── applications.html     <-- Consolidated tracking tables
│       ├── profile.html          <-- Custom profile tag editors
│       ├── recommendations.html  <-- AI-driven detailed skills analyzer
│       └── users.html            <-- Administrative console
├── .env.example                  <-- Secret templates
├── .env                          <-- Environment variables
└── .gitignore                    <-- Git exclusion parameters
```
