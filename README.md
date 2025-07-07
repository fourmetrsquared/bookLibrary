# 📚 Online Book Library and Reader

A Django-powered web application for managing and reading books online.

## 🚀 Features

- 📖 Add, edit, and delete books
- 👁️‍🗨️ Read books in-browser with pagination
- 🗃️ Organize books by category or author
- 🔍 Search functionality
- 🧑‍💻 Admin dashboard for managing content
- 🌐 User authentication (sign up, login, logout)
- 📥 Upload PDFs and cover images

## 🛠 Tech Stack

- **Backend:** Django, SQLite/PostgreSQL
- **Frontend:** HTML, CSS (Bootstrap/Tailwind), JavaScript
- **Other:** Django Admin, Django REST (optional for API)

## 📦 Installation

```bash
git clone https://github.com/fourmetrsquared/bookLibrary.git
cd bookLibrary
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
