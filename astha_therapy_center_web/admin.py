from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Article, Appointment, Contact, Therapist


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin configuration
    """
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Article)

# Register Appointment model for Django admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'service', 'appointment_date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Appointment Details', {
            'fields': ('service', 'appointment_date', 'status', 'notes')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Register Contact model for Django admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message Details', {
            'fields': ('message', 'status')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    actions = ['mark_as_read', 'mark_as_replied']


# Register Therapist model for Django admin
@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'experience_years', 'email', 'is_active', 'display_order']
    list_filter = ['is_active', 'experience_years', 'created_at']
    search_fields = ['name', 'title', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 20
    list_editable = ['is_active', 'display_order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'experience_years', 'email', 'phone')
        }),
        ('Profile Content', {
            'fields': ('bio_short', 'bio_full', 'personal_info', 'awards_info')
        }),
        ('Media', {
            'fields': ('profile_image',)
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Professional Skills', {
            'fields': (
                'skill_patient_diagnosis', 'skill_treatment_planning', 
                'skill_manual_therapy', 'skill_exercise_prescription',
                'skill_electrotherapy', 'skill_interpersonal'
            ),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('display_order', 'name')
