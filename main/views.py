# main/views.py
# -*- coding: utf-8 -*-
from django.shortcuts import render
from hospitals.models import Category

def main_page1_view(request):
    context = {'my_variable': 'Hello from Main Page 1!'}
    return render(request, 'main/main_page1.html', context)

def main_page2_view(request):
    categories = Category.objects.all()
    context = {'my_variable': 'Hello from Main Page 2!', 'categories': categories}
    return render(request, 'main/main_page2.html', context)
