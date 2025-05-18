# 🧠 Online Code Compiler 💻

An online code compiler built using **Django**, allowing users to write, submit, and execute code in **C**, **C++**, and **Python** — all from the browser!

---

## ✨ Features

- ✅ Supports C, C++, and Python
- 📥 Takes custom input
- ⚡ Executes code and returns output instantly
- 💾 Stores submissions in a database
- 🧹 Cleans up temporary files after execution
- 🚫 Handles compile errors, runtime errors, and timeouts gracefully

---

## 🛠️ Tech Stack

- Backend: **Django**
- Language Execution: `subprocess` module (with timeout and error handling)
- Database: **SQLite** (default for development)
- Frontend: HTML, CSS (basic UI)

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
https://github.com/codesayan2004/compiler.git
cd compiler
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

