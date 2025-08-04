from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Appointment, Contact, Therapist

# Get the custom user model
User = get_user_model()

# Create your views here.

def home(request):
    return render(request, 'web/index.html')

def about(request):
    return render(request, 'web/about.html')

def service(request):
    return render(request, 'web/service.html')

def therapist(request):
    therapists = Therapist.objects.filter(is_active=True).order_by('display_order', 'name')
    context = {
        'therapists': therapists,
    }
    return render(request, 'web/therapist.html', context)

def contact(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('msg')
            
            # Debug print to see what data we're getting
            print(f"DEBUG - Contact form data received:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Phone: {phone}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            
            # Validate required fields
            if not name or not email or not phone or not subject or not message:
                messages.error(request, 'Please fill in all required fields.')
                return redirect('astha_therapy_center_web:contact')
            
            # Create and save contact message
            contact_message = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                status='new'
            )
            
            print(f"DEBUG - Contact message created successfully: {contact_message.id}")
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('astha_therapy_center_web:contact')
            
        except Exception as e:
            print(f"DEBUG - Error creating contact message: {str(e)}")
            messages.error(request, f'There was an error sending your message: {str(e)}')
            return redirect('astha_therapy_center_web:contact')
    
    return render(request, 'web/contact.html')

def blogs(request):
    return render(request, 'web/blog.html')

def blog(request):
    return render(request, 'web/blog-single.html')

def faqs(request):
    return render(request, 'web/faqs.html')

def testimonials(request):
    return render(request, 'web/testimonials.html')

def therapist_single(request, therapist_id):
    """View for individual therapist detail page"""
    try:
        therapist = Therapist.objects.get(id=therapist_id, is_active=True)
    except Therapist.DoesNotExist:
        return render(request, 'web/404.html', status=404)
    
    context = {
        'therapist': therapist,
    }
    return render(request, 'web/therapist-single.html', context)



def appointment(request):
    if request.method == 'POST':
        try:
            # Extract form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            service = request.POST.get('services')
            date = request.POST.get('date')
            
            # Debug print to see what data we're getting
            print(f"DEBUG - Form data received:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Phone: {phone}")
            print(f"Service: {service}")
            print(f"Date: {date}")
            
            # Validate required fields
            if not name or not email or not phone or not service or not date:
                messages.error(request, 'Please fill in all required fields.')
                return redirect('astha_therapy_center_web:appointment')
            
            # Create and save appointment
            appointment = Appointment.objects.create(
                name=name,
                email=email,
                phone=phone,
                service=service,
                appointment_date=date,
                status='pending'
            )
            
            print(f"DEBUG - Appointment created successfully: {appointment.id}")
            messages.success(request, 'Your appointment has been booked successfully! We will contact you soon.')
            return redirect('astha_therapy_center_web:appointment')
            
        except Exception as e:
            print(f"DEBUG - Error creating appointment: {str(e)}")
            messages.error(request, f'There was an error booking your appointment: {str(e)}')
            return redirect('astha_therapy_center_web:appointment')
    
    from datetime import date
    context = {
        'today': date.today()
    }
    return render(request, 'web/appointment.html', context)


# Custom Forms for Email Authentication
class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': True
        })
    )




# Authentication Views
def user_login(request):
    """
    Custom login view using email instead of username
    """
    if request.user.is_authenticated:
        return redirect('astha_therapy_center_web:home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate using email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
                
                # Redirect to therapy admin dashboard
                return redirect('astha_therapy_center_web:therapy_admin')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})





def user_logout(request):
    """
    Logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('astha_therapy_center_web:home')


@login_required
def therapy_admin(request):
    """
    Therapy admin dashboard (requires login)
    """
    # Get statistics for dashboard
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    total_contacts = Contact.objects.count()
    new_contacts = Contact.objects.filter(status='new').count()
    total_therapists = Therapist.objects.filter(is_active=True).count()
    
    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'total_contacts': total_contacts,
        'new_contacts': new_contacts,
        'total_therapists': total_therapists,
    }
    
    return render(request, 'admin/dashboard.html', context)


def sitemap(request):
    """
    Generate XML sitemap for search engines
    """
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from datetime import datetime
    
    # Get current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define static pages with their priorities and change frequencies
    pages = [
        {'url': '', 'priority': '1.0', 'changefreq': 'weekly', 'lastmod': current_date},
        {'url': 'about/', 'priority': '0.8', 'changefreq': 'monthly', 'lastmod': current_date},
        {'url': 'service/', 'priority': '0.8', 'changefreq': 'monthly', 'lastmod': current_date},
        {'url': 'therapist/', 'priority': '0.7', 'changefreq': 'weekly', 'lastmod': current_date},
        {'url': 'contact/', 'priority': '0.6', 'changefreq': 'monthly', 'lastmod': current_date},
        {'url': 'appointment/', 'priority': '0.9', 'changefreq': 'weekly', 'lastmod': current_date},
        {'url': 'blogs/', 'priority': '0.6', 'changefreq': 'weekly', 'lastmod': current_date},
        {'url': 'faqs/', 'priority': '0.5', 'changefreq': 'monthly', 'lastmod': current_date},
        {'url': 'testimonials/', 'priority': '0.5', 'changefreq': 'monthly', 'lastmod': current_date},
    ]
    
    context = {
        'pages': pages,
        'current_date': current_date,
    }
    
    # Generate XML sitemap
    xml_content = render_to_string('sitemap.xml', context)
    
    # Return XML response
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Type'] = 'application/xml; charset=utf-8'
    return response



