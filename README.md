# CodeQuest 🎮

A gamified e-learning platform built with Django and Django REST Framework. Learners earn XP, level up, and collect badges as they complete lessons.

🔗 **Live Demo:** https://codequest-ak4q.onrender.com

---

## Features

- 🔐 User authentication with role-based access (Learner / Admin)
- 🎯 Gamification system — XP points, levels, and badges on lesson completion
- 📚 Course and lesson management with structured content
- ⚡ RESTful API built with Django REST Framework and nested serializers
- 🗄️ 10+ relational database models (OneToOne, ForeignKey, ManyToMany)
- 📱 Responsive frontend with HTML, CSS, and JavaScript
- 🚀 Deployed on Render

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite (local) |
| Auth | Django built-in authentication |
| Deployment | Render |
| Static Files | WhiteNoise |

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

Clone the repo

    git clone https://github.com/Kusum06101/CodeQuest.git
    cd CodeQuest

Create and activate virtual environment

    python -m venv venv
    venv\Scripts\activate

Install dependencies

    pip install -r requirements.txt

Create a `.env` file in the root folder and add

    SECRET_KEY=your-secret-key-here
    DEBUG=True

Run migrations

    python manage.py migrate

Start the server

    python manage.py runserver

Visit http://127.0.0.1:8000

---

## Project Structure

    CodeQuest/
    ├── base/               Main app — models, views, serializers
    ├── myproject/          Django settings and URLs
    ├── templates/          HTML templates
    ├── static/             CSS, JS, images
    ├── requirements.txt    Dependencies
    └── manage.py

---

## Author

**Kusum C** — Full Stack Developer

- 💼 LinkedIn: https://www.linkedin.com/in/kusum-c
- 🐙 GitHub: https://github.com/Kusum06101
