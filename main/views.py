# main/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render
from hospitals.models import Category
from health_tips.models import Post

def main_page1_view(request):
    posts=Post.objects.filter(is_banner=True)
    context = {'my_variable': 'Hello from Main Page 1!', 'posts': posts}
    return render(request, 'main/main_page1.html', context)

def main_page2_view(request, posts=None):
    posts = Post.objects.filter(is_banner=True)
    categories = Category.objects.all()
    context = {'my_variable': 'Hello from Main Page 2!', 'categories': categories, 'posts': posts}
    return render(request, 'main/main_page2.html', context)