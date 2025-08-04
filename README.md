# Astha Therapy Center

A comprehensive Django web application for a therapy center with appointment booking, therapist management, and blog system.

## Features

- **Appointment Booking System** - Patients can book therapy sessions online
- **Therapist Management** - Complete therapist profiles with skills and experience
- **Blog System** - Content management with categories and tags
- **Contact Form** - Patient inquiry management
- **Admin Dashboard** - Full administrative interface
- **Responsive Design** - Mobile-friendly interface

## Tech Stack

- **Backend**: Django 5.2
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Custom email-based user system

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sorkerlimon/AsthaTherapyCenter.git
   cd AsthaTherapyCenter
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Therapy Admin**: http://localhost:8000/therapy_admin

## Project Structure

```
AsthaTherapyCenter/
├── astha_therapy_center_web/    # Main Django app
├── templates/                   # HTML templates
├── static/                     # CSS, JS, images
├── media/                      # User uploaded files
└── requirements.txt            # Python dependencies
```

## License

This project is private and proprietary. 