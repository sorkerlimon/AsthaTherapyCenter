import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username
    """
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name


class Appointment(models.Model):
    """
    Model for storing appointment bookings
    """
    SERVICE_CHOICES = [
        ('manual_therapy', 'Manual Therapy'),
        ('chronic_pain', 'Chronic Pain'),
        ('hand_therapy', 'Hand Therapy'),
        ('sports_therapy', 'Sports Therapy'),
        ('cupping_therapy', 'Cupping Therapy'),
        ('ultrasound_therapy', 'Ultrasound Therapy'),
        ('laser_therapy', 'Laser Therapy'),
        ('craniosacral_therapy', 'Craniosacral Therapy'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
    
    def __str__(self):
        return f"{self.name} - {self.get_service_display()} on {self.appointment_date}"
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'pending': 'bg-warning',
            'confirmed': 'bg-info',
            'completed': 'bg-success',
            'cancelled': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')


class Contact(models.Model):
    """
    Model for storing contact form submissions
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def get_status_badge_class(self):
        """Return CSS class for status badge"""
        status_classes = {
            'new': 'bg-primary',
            'read': 'bg-info',
            'replied': 'bg-success',
            'closed': 'bg-secondary',
        }
        return status_classes.get(self.status, 'bg-secondary')


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/')
    
    def __str__(self):
        return self.title


class Therapist(models.Model):
    """
    Model for therapist/doctor profiles
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Full name (e.g., Dr. Emily Johnson)")
    title = models.CharField(max_length=100, help_text="Professional title (e.g., Senior Physiotherapist)")
    experience_years = models.PositiveIntegerField(help_text="Years of experience")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Profile and content
    bio_short = models.TextField(max_length=500, help_text="Short bio for cards and lists")
    bio_full = models.TextField(help_text="Full biography for detail page")
    personal_info = models.TextField(blank=True, null=True, help_text="Personal information section")
    awards_info = models.TextField(blank=True, null=True, help_text="Awards and honors information")
    
    # Images
    profile_image = models.ImageField(upload_to='therapist_images/', help_text="Main profile photo")
    
    # Social media links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Professional skills (percentage out of 100)
    skill_patient_diagnosis = models.PositiveIntegerField(default=0, help_text="Patient diagnosis skill percentage (0-100)")
    skill_treatment_planning = models.PositiveIntegerField(default=0, help_text="Treatment planning skill percentage (0-100)")
    skill_manual_therapy = models.PositiveIntegerField(default=0, help_text="Manual therapy techniques skill percentage (0-100)")
    skill_exercise_prescription = models.PositiveIntegerField(default=0, help_text="Exercise prescription skill percentage (0-100)")
    skill_electrotherapy = models.PositiveIntegerField(default=0, help_text="Electrotherapy skill percentage (0-100)")
    skill_interpersonal = models.PositiveIntegerField(default=0, help_text="Interpersonal skills percentage (0-100)")
    
    # Status and display
    is_active = models.BooleanField(default=True, help_text="Whether this therapist profile should be displayed")
    display_order = models.PositiveIntegerField(default=0, help_text="Order for displaying therapists (lower numbers first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Therapist'
        verbose_name_plural = 'Therapists'
    
    def __str__(self):
        return f"{self.name} - {self.title}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('astha_therapy_center_web:therapist_single', kwargs={'therapist_id': self.id})
    
    def get_experience_display(self):
        """Return formatted experience string"""
        if self.experience_years == 1:
            return "01 Year"
        return f"{self.experience_years:02d} Years"
    
    def get_skills_data(self):
        """Return skills as a list of dictionaries for template iteration"""
        return [
            {'name': 'patient diagnosis', 'percentage': self.skill_patient_diagnosis},
            {'name': 'treatment planning', 'percentage': self.skill_treatment_planning},
            {'name': 'manual therapy techniques', 'percentage': self.skill_manual_therapy},
            {'name': 'exercise prescription', 'percentage': self.skill_exercise_prescription},
            {'name': 'electrotherapy skill', 'percentage': self.skill_electrotherapy},
            {'name': 'interpersonal skills', 'percentage': self.skill_interpersonal},
        ]
    
    def clean(self):
        """Validate skill percentages are between 0 and 100"""
        from django.core.exceptions import ValidationError
        skills = [
            self.skill_patient_diagnosis, self.skill_treatment_planning,
            self.skill_manual_therapy, self.skill_exercise_prescription,
            self.skill_electrotherapy, self.skill_interpersonal
        ]
        for skill in skills:
            if skill < 0 or skill > 100:
                raise ValidationError('Skill percentages must be between 0 and 100.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
