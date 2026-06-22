# CodeQuest 🎮

A gamified e-learning platform built with Django and Django REST Framework. Learners earn XP, level up, and collect badges as they complete lessons.

🔗 **Live Demo:** https://codequest-ak4q.onrender.com

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-092E20?style=for-the-badge&logo=django&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
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
## Screenshots

### Homepage
*The space-themed landing page*
<img width="1920" height="906" alt="homepage" src="https://github.com/user-attachments/assets/6d17c696-2c20-4735-a85d-618481aba318" />


### Course Catalog
*Browse available courses*
<img width="1916" height="896" alt="course-catalog" src="https://github.com/user-attachments/assets/f10df6fb-e947-44c5-ba9b-8391f34ad03a" />


### Dashboard
*Track your progress*
<img width="1914" height="912" alt="dashboard" src="https://github.com/user-attachments/assets/ff9fef12-4c51-44fc-9c34-9aa136c4f596" />


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
