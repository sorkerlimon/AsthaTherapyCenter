from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django import forms
from .models import Appointment, Contact, Therapist
import json
from datetime import datetime


class AppointmentForm(forms.ModelForm):
    """
    Form for creating and editing appointments
    """
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'service', 'appointment_date', 'status', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }


@login_required
def admin_dashboard(request):
    """
    Main admin dashboard with overview statistics
    """
    # Get appointment statistics
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    confirmed_appointments = Appointment.objects.filter(status='confirmed').count()
    completed_appointments = Appointment.objects.filter(status='completed').count()
    
    # Get contact statistics
    total_contacts = Contact.objects.count()
    new_contacts = Contact.objects.filter(status='new').count()
    read_contacts = Contact.objects.filter(status='read').count()
    replied_contacts = Contact.objects.filter(status='replied').count()
    
    # Recent appointments
    recent_appointments = Appointment.objects.all()[:5]
    
    # Recent contact messages
    recent_contacts = Contact.objects.all()[:5]
    
    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'total_contacts': total_contacts,
        'new_contacts': new_contacts,
        'read_contacts': read_contacts,
        'replied_contacts': replied_contacts,
        'recent_appointments': recent_appointments,
        'recent_contacts': recent_contacts,
    }
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
def appointment_list(request):
    """
    List all appointments with search and filtering
    """
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    appointments = Appointment.objects.all()
    
    # Apply search filter
    if search_query:
        appointments = appointments.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(appointments, 10)  # Show 10 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Appointment.STATUS_CHOICES,
    }
    return render(request, 'admin/appointment_list.html', context)


@login_required
def appointment_create(request):
    """
    Create new appointment
    """
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment for {appointment.name} created successfully!')
            return redirect('astha_therapy_center_web:admin_appointment_list')
    else:
        form = AppointmentForm()
    
    context = {'form': form, 'title': 'Create New Appointment'}
    return render(request, 'admin/appointment_form.html', context)


@login_required
def appointment_detail(request, appointment_id):
    """
    View appointment details
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {'appointment': appointment}
    return render(request, 'admin/appointment_detail.html', context)


@login_required
def appointment_edit(request, appointment_id):
    """
    Edit existing appointment
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment for {appointment.name} updated successfully!')
            return redirect('astha_therapy_center_web:admin_appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
        'title': f'Edit Appointment - {appointment.name}'
    }
    return render(request, 'admin/appointment_form.html', context)


@login_required
def appointment_delete(request, appointment_id):
    """
    Delete appointment
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        patient_name = appointment.name
        appointment.delete()
        messages.success(request, f'Appointment for {patient_name} deleted successfully!')
        return redirect('astha_therapy_center_web:admin_appointment_list')
    
    context = {'appointment': appointment}
    return render(request, 'admin/appointment_delete.html', context)


@login_required
@require_http_methods(["POST"])
def appointment_update_status(request, appointment_id):
    """
    AJAX endpoint to update appointment status
    """
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Status updated to {appointment.get_status_display()}',
                'new_status': new_status,
                'badge_class': appointment.get_status_badge_class()
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def appointment_statistics(request):
    """
    Appointment statistics and analytics
    """
    from django.db.models import Count
    from collections import defaultdict
    
    # Status distribution
    status_stats = Appointment.objects.values('status').annotate(count=Count('status'))
    
    # Service distribution
    service_stats = Appointment.objects.values('service').annotate(count=Count('service'))
    
    # Monthly appointments (last 6 months)
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth
    
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_stats = (Appointment.objects
                    .filter(created_at__gte=six_months_ago)
                    .annotate(month=TruncMonth('created_at'))
                    .values('month')
                    .annotate(count=Count('id'))
                    .order_by('month'))
    
    context = {
        'status_stats': status_stats,
        'service_stats': service_stats,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'admin/appointment_statistics.html', context)


# =============================================================================
# CONTACT MANAGEMENT VIEWS
# =============================================================================

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


@login_required
def contact_list(request):
    """
    Display list of all contact messages with search and filter
    """
    contact_list = Contact.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        contact_list = contact_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        contact_list = contact_list.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(contact_list, 10)  # 10 contacts per page
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    
    # Get status choices for filter dropdown
    status_choices = Contact.STATUS_CHOICES
    
    context = {
        'contacts': contacts,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    return render(request, 'admin/contact_list.html', context)


@login_required
def contact_detail(request, contact_id):
    """
    Display contact message details
    """
    contact = get_object_or_404(Contact, id=contact_id)
    
    # Mark as read when viewed
    if contact.status == 'new':
        contact.status = 'read'
        contact.save()
    
    return render(request, 'admin/contact_detail.html', {'contact': contact})


@login_required
def contact_edit(request, contact_id):
    """
    Edit contact message (mainly for status updates)
    """
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact message updated successfully!')
            return redirect('astha_therapy_center_web:admin_contact_detail', contact_id=contact.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'admin/contact_form.html', {
        'form': form,
        'contact': contact,
        'action': 'Edit'
    })


@login_required
def contact_delete(request, contact_id):
    """
    Delete contact message
    """
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted successfully!')
        return redirect('astha_therapy_center_web:admin_contact_list')
    
    return render(request, 'admin/contact_delete.html', {'contact': contact})


@login_required
@require_http_methods(["POST"])
def contact_update_status(request, contact_id):
    """
    AJAX endpoint to update contact status
    """
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in [choice[0] for choice in Contact.STATUS_CHOICES]:
            contact.status = new_status
            contact.save()
            return JsonResponse({
                'success': True, 
                'message': f'Status updated to {contact.get_status_display()}',
                'new_status': new_status,
                'badge_class': contact.get_status_badge_class()
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def contact_statistics(request):
    """
    Contact statistics and analytics
    """
    from django.db.models import Count
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth
    
    # Status distribution
    status_stats = Contact.objects.values('status').annotate(count=Count('status'))
    
    # Monthly contacts (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_stats = (Contact.objects
                    .filter(created_at__gte=six_months_ago)
                    .annotate(month=TruncMonth('created_at'))
                    .values('month')
                    .annotate(count=Count('id'))
                    .order_by('month'))
    
    context = {
        'status_stats': status_stats,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'admin/contact_statistics.html', context)


# =============================================================================
# THERAPIST MANAGEMENT VIEWS
# =============================================================================

class TherapistForm(forms.ModelForm):
    """
    Form for creating and editing therapists
    """
    class Meta:
        model = Therapist
        fields = [
            'name', 'title', 'experience_years', 'email', 'phone',
            'bio_short', 'bio_full', 'personal_info', 'awards_info',
            'profile_image', 'facebook_url', 'twitter_url', 'instagram_url',
            'youtube_url', 'linkedin_url', 'skill_patient_diagnosis',
            'skill_treatment_planning', 'skill_manual_therapy',
            'skill_exercise_prescription', 'skill_electrotherapy',
            'skill_interpersonal', 'is_active', 'display_order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name (e.g., Dr. Emily Johnson)'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Professional Title (e.g., Senior Physiotherapist)'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '50'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (optional)'}),
            'bio_short': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short bio for cards and lists (max 500 characters)'}),
            'bio_full': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Full biography for detail page'}),
            'personal_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Personal information section (optional)'}),
            'awards_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Awards and honors information (optional)'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook URL (optional)'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter/X URL (optional)'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram URL (optional)'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'YouTube URL (optional)'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn URL (optional)'}),
            'skill_patient_diagnosis': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'skill_treatment_planning': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'skill_manual_therapy': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'skill_exercise_prescription': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'skill_electrotherapy': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'skill_interpersonal': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'placeholder': '0-100'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Display order (lower numbers first)'}),
        }


@login_required
def therapist_list(request):
    """
    List all therapists with search and filtering
    """
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    therapists = Therapist.objects.all()
    
    # Apply search filter
    if search_query:
        therapists = therapists.filter(
            Q(name__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        if status_filter == 'active':
            therapists = therapists.filter(is_active=True)
        elif status_filter == 'inactive':
            therapists = therapists.filter(is_active=False)
    
    # Order by display_order and name
    therapists = therapists.order_by('display_order', 'name')
    
    # Pagination
    paginator = Paginator(therapists, 10)  # Show 10 therapists per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': [('active', 'Active'), ('inactive', 'Inactive')],
    }
    return render(request, 'admin/therapist_list.html', context)


@login_required
def therapist_create(request):
    """
    Create new therapist
    """
    if request.method == 'POST':
        form = TherapistForm(request.POST, request.FILES)
        if form.is_valid():
            therapist = form.save()
            messages.success(request, f'Therapist {therapist.name} created successfully!')
            return redirect('astha_therapy_center_web:admin_therapist_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TherapistForm()
    
    context = {'form': form, 'title': 'Create New Therapist'}
    return render(request, 'admin/therapist_form.html', context)


@login_required
def therapist_detail(request, therapist_id):
    """
    View therapist details
    """
    therapist = get_object_or_404(Therapist, id=therapist_id)
    context = {'therapist': therapist}
    return render(request, 'admin/therapist_detail.html', context)


@login_required
def therapist_edit(request, therapist_id):
    """
    Edit existing therapist
    """
    therapist = get_object_or_404(Therapist, id=therapist_id)
    
    if request.method == 'POST':
        form = TherapistForm(request.POST, request.FILES, instance=therapist)
        if form.is_valid():
            therapist = form.save()
            messages.success(request, f'Therapist {therapist.name} updated successfully!')
            return redirect('astha_therapy_center_web:admin_therapist_detail', therapist_id=therapist.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TherapistForm(instance=therapist)
    
    context = {
        'form': form,
        'therapist': therapist,
        'title': f'Edit Therapist - {therapist.name}'
    }
    return render(request, 'admin/therapist_form.html', context)


@login_required
def therapist_delete(request, therapist_id):
    """
    Delete therapist
    """
    therapist = get_object_or_404(Therapist, id=therapist_id)
    
    if request.method == 'POST':
        therapist_name = therapist.name
        therapist.delete()
        messages.success(request, f'Therapist {therapist_name} deleted successfully!')
        return redirect('astha_therapy_center_web:admin_therapist_list')
    
    context = {'therapist': therapist}
    return render(request, 'admin/therapist_delete.html', context)


@login_required
@require_http_methods(["POST"])
def therapist_update_status(request, therapist_id):
    """
    AJAX endpoint to update therapist active status
    """
    try:
        therapist = get_object_or_404(Therapist, id=therapist_id)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in ['active', 'inactive']:
            therapist.is_active = (new_status == 'active')
            therapist.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Status updated to {"Active" if therapist.is_active else "Inactive"}',
                'new_status': 'active' if therapist.is_active else 'inactive',
                'badge_class': 'badge-success' if therapist.is_active else 'badge-secondary'
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid status'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def therapist_statistics(request):
    """
    Therapist statistics and analytics
    """
    from django.db.models import Count, Avg
    
    # Active vs inactive therapists
    active_count = Therapist.objects.filter(is_active=True).count()
    inactive_count = Therapist.objects.filter(is_active=False).count()
    
    # Average experience years
    avg_experience = Therapist.objects.filter(is_active=True).aggregate(
        avg_experience=Avg('experience_years')
    )['avg_experience'] or 0
    
    # Skills statistics
    skills_stats = {
        'patient_diagnosis': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_patient_diagnosis')
        )['avg'] or 0,
        'treatment_planning': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_treatment_planning')
        )['avg'] or 0,
        'manual_therapy': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_manual_therapy')
        )['avg'] or 0,
        'exercise_prescription': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_exercise_prescription')
        )['avg'] or 0,
        'electrotherapy': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_electrotherapy')
        )['avg'] or 0,
        'interpersonal': Therapist.objects.filter(is_active=True).aggregate(
            avg=Avg('skill_interpersonal')
        )['avg'] or 0,
    }
    
    context = {
        'active_count': active_count,
        'inactive_count': inactive_count,
        'total_therapists': active_count + inactive_count,
        'avg_experience': round(avg_experience, 1),
        'skills_stats': skills_stats,
    }
    return render(request, 'admin/therapist_statistics.html', context)