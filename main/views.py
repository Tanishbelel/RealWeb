from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
import requests
import json
from .models import *

def home(request):
    context = {
        'profile': Profile.objects.first(),
        'featured_skills': Skill.objects.filter(is_featured=True)[:6],
        'featured_projects': Project.objects.filter(is_featured=True)[:3],
        'featured_certificates': Certificate.objects.filter(is_featured=True)[:3],
        'recent_experience': Experience.objects.first(),
        'linkedin_posts': LinkedInPost.objects.filter(is_active=True)[:3],
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'profile': Profile.objects.first(),
        'featured_skills': Skill.objects.filter(is_featured=True),
        'education': Education.objects.all(),
        'experience': Experience.objects.all(),
    }
    return render(request, 'about.html', context)

def projects(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'projects.html', context)

def certificates(request):
    context = {
        'certificates': Certificate.objects.all().order_by('-issue_date'),
    }
    return render(request, 'certificates.html', context)

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return JsonResponse({'status': 'success'})
    
    context = {
        'profile': Profile.objects.first(),
    }
    return render(request, 'contact.html', context)

# LinkedIn API Integration
def fetch_linkedin_posts():
    """Fetch latest LinkedIn posts"""
    if not settings.LINKEDIN_ACCESS_TOKEN:
        return []
    
    headers = {
        'Authorization': f'Bearer {settings.LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    # LinkedIn API endpoint for user posts
    url = f'https://api.linkedin.com/v2/shares?q=owners&owners={settings.LINKEDIN_PERSON_URN}&count=5'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            posts = []
            
            for post in data.get('elements', []):
                post_data = {
                    'post_id': post.get('id'),
                    'content': post.get('text', {}).get('text', ''),
                    'created_at': post.get('created', {}).get('time'),
                    'post_url': f"https://www.linkedin.com/feed/update/{post.get('id')}"
                }
                posts.append(post_data)
            
            return posts
    except Exception as e:
        print(f"Error fetching LinkedIn posts: {e}")
    
    return []

def update_linkedin_posts(request):
    """Admin view to update LinkedIn posts"""
    if request.user.is_staff:
        posts = fetch_linkedin_posts()
        updated_count = 0
        
        for post_data in posts:
            post, created = LinkedInPost.objects.get_or_create(
                post_id=post_data['post_id'],
                defaults=post_data
            )
            if created:
                updated_count += 1
        
        return JsonResponse({
            'status': 'success',
            'message': f'Updated {updated_count} new posts'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Unauthorized'})