from django.contrib import admin
from students.models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'phone',
        # 'view_link',
    ]
    search_fields = ['name', 'phone']

    # actions = [search.signals.reindex]

