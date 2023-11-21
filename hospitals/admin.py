from django.contrib import admin
from .models import Hospital, Category, Review

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Category)
admin.site.register(Review)