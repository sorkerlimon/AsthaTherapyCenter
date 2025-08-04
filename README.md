# 🏥 Aastha Therapy Center

A comprehensive Django-based therapy center website with appointment booking, therapist management, and admin dashboard. Built with modern web technologies and optimized for pediatric therapy services.

## 🌟 Features

### **Public Features**
- **Responsive Design**: Modern, mobile-friendly interface
- **Appointment Booking**: Online appointment scheduling system
- **Therapist Profiles**: Detailed therapist information and skills
- **Service Showcase**: Comprehensive therapy services display
- **Contact Management**: Multi-channel contact system
- **Blog Section**: Content marketing area
- **Testimonials**: Client feedback system
- **SEO Optimized**: Sitemap and robots.txt included

### **Admin Features**
- **Dashboard**: Comprehensive admin dashboard with statistics
- **Appointment Management**: Full CRUD operations for appointments
- **Contact Management**: Message handling and status tracking
- **Therapist Management**: Profile creation and editing
- **Status Management**: Real-time status updates
- **Email Authentication**: Secure admin login system

### **Technical Features**
- **Custom User Model**: Email-based authentication
- **UUID Primary Keys**: Secure and scalable
- **Image Handling**: Proper image upload functionality
- **Form Validation**: Client and server-side validation
- **Responsive Design**: Bootstrap-based responsive layout
- **Static File Optimization**: Whitenoise for production

## 🛠️ Technology Stack

### **Backend**
- **Django 5.2.4**: Python web framework
- **MySQL**: Database management
- **Python 3.13.3**: Programming language

### **Frontend**
- **Bootstrap**: Responsive CSS framework
- **jQuery**: JavaScript library
- **Font Awesome**: Icon library
- **GSAP**: Animation library
- **Swiper**: Touch slider

### **Deployment**
- **Whitenoise**: Static file serving
- **Django Sites Framework**: Site management
- **Environment Variables**: Secure configuration

## 📁 Project Structure

```
AsthaTherapyCenter/
├── aastha_therapy_center/          # Django project settings
├── astha_therapy_center_web/       # Main Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # Public views
│   ├── views_admin.py              # Admin views
│   ├── urls.py                     # URL routing
│   └── admin.py                    # Admin configuration
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── web/                        # Public pages
│   ├── admin/                      # Admin pages
│   └── authentication/             # Login pages
├── static/                         # Static files
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript files
│   └── images/                     # Images and icons
├── media/                          # User uploads
├── requirements.txt                # Python dependencies
├── robots.txt                      # SEO robots file
└── templates/sitemap.xml          # SEO sitemap
```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.13+
- MySQL Database
- Virtual Environment

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd AsthaTherapyCenter
```

### **2. Create Virtual Environment**
```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
Create a `.env` file in the root directory:
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=astha_therapy
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,asthatherapycenter.com

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### **5. Database Setup**
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### **6. Collect Static Files**
```bash
python manage.py collectstatic
```

### **7. Run Development Server**
```bash
python manage.py runserver
```

## 🌐 Access URLs

### **Public Pages**
- **Homepage**: `http://localhost:8000/`
- **About**: `http://localhost:8000/about/`
- **Services**: `http://localhost:8000/service/`
- **Therapists**: `http://localhost:8000/therapist/`
- **Contact**: `http://localhost:8000/contact/`
- **Appointment**: `http://localhost:8000/appointment/`
- **Blog**: `http://localhost:8000/blogs/`
- **FAQs**: `http://localhost:8000/faqs/`
- **Testimonials**: `http://localhost:8000/testimonials/`

### **Admin Pages**
- **Admin Login**: `http://localhost:8000/login/`
- **Dashboard**: `http://localhost:8000/therapy_admin/`
- **Appointments**: `http://localhost:8000/therapy_admin/appointments/`
- **Contacts**: `http://localhost:8000/therapy_admin/contacts/`
- **Therapists**: `http://localhost:8000/therapy_admin/therapists/`

### **SEO Files**
- **robots.txt**: `http://localhost:8000/robots.txt`
- **sitemap.xml**: `http://localhost:8000/sitemap.xml`

## 📊 Database Models

### **CustomUser**
- Email-based authentication
- Custom user manager
- Profile information

### **Appointment**
- UUID primary key
- Service selection
- Status tracking (pending, confirmed, completed, cancelled)
- Date and time management

### **Contact**
- Message handling
- Status tracking (new, read, replied, closed)
- Contact information

### **Therapist**
- Detailed profiles
- Skill assessments
- Social media links
- Professional information

## 🎨 Design Features

### **UI/UX**
- **Modern Design**: Professional therapy center aesthetic
- **Bilingual Support**: English and Bengali content
- **Smooth Animations**: GSAP-powered animations
- **Interactive Elements**: Hero sliders, testimonials
- **Responsive Layout**: Mobile-first design

### **Color Scheme**
- Primary: Professional blue tones
- Secondary: Warm therapy colors
- Accent: Highlight colors for CTAs

## 🔧 Configuration

### **Settings Configuration**
- **ALLOWED_HOSTS**: Configured for local and production
- **STATIC_FILES**: Whitenoise for production serving
- **DATABASE**: MySQL with proper charset
- **SITE_ID**: Django Sites Framework enabled

### **SEO Configuration**
- **Sitemap**: Auto-generated XML sitemap
- **Robots.txt**: Search engine directives
- **Meta Tags**: SEO-optimized meta information

## 🚀 Deployment

### **Production Checklist**
1. Set `DEBUG = False`
2. Configure production database
3. Set secure `SECRET_KEY`
4. Configure `ALLOWED_HOSTS`
5. Set up email backend
6. Run `python manage.py collectstatic`
7. Configure web server (nginx/Apache)
8. Set up SSL certificate

### **Environment Variables**
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=asthatherapycenter.com,www.asthatherapycenter.com
```

## 📱 Mobile Responsiveness

The website is fully responsive and optimized for:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly interface

## 🔒 Security Features

- **CSRF Protection**: Enabled by default
- **SQL Injection Protection**: Django ORM
- **XSS Protection**: Template escaping
- **Secure Authentication**: Custom user model
- **Admin Protection**: Login required for admin areas

## 📈 Performance Optimization

- **Static File Compression**: Whitenoise
- **Image Optimization**: Proper image handling
- **Database Optimization**: Efficient queries
- **Caching**: Static file caching
- **CDN Ready**: Static files optimized for CDN

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Developed by [Sorker Limon](https://github.com/sorkerlimon)**

- **GitHub**: [@sorkerlimon](https://github.com/sorkerlimon)
- **Skills**: DevOps, Cloud Engineering, System Administration, Backend Development
- **Experience**: 3+ years in DevOps and development

## 📞 Support

For support or questions:
- **Email**: sorkerlimon18@gmail.com
- **Phone**: +8801635200923
- **GitHub**: [https://github.com/sorkerlimon](https://github.com/sorkerlimon)

---

**© 2025 Aastha Therapy Center. All Rights Reserved.**
