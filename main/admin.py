from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'updated_at']
    fields = ['name', 'title', 'email', 'phone', 'location', 'bio', 
              'profile_image', 'resume', 'linkedin_url', 'github_url']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_featured']
    list_filter = ['category', 'is_featured']
    list_editable = ['proficiency', 'is_featured']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'technologies', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    list_editable = ['is_featured']
    search_fields = ['title', 'description', 'technologies']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'is_featured', 'certificate_preview']
    list_filter = ['issuer', 'is_featured', 'issue_date']
    list_editable = ['is_featured']
    search_fields = ['title', 'issuer']
    date_hierarchy = 'issue_date'
    
    def certificate_preview(self, obj):
        if obj.certificate_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.certificate_image.url
            )
        return "No Image"
    certificate_preview.short_description = "Preview"

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    list_editable = ['is_current']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date']
    list_filter = ['start_date']

@admin.register(LinkedInPost)
class LinkedInPostAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'like_count', 'comment_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    readonly_fields = ['post_id', 'content', 'created_at', 'like_count', 'comment_count', 'post_url']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    search_fields = ['name', 'email', 'subject']