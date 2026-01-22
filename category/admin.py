from django.contrib import admin
from .models import Category

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name')

    list_filter = ('id',)
    ordering = ('id',)


admin.site.register(Category, AdminCategory)
