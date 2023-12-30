from django.contrib import admin
from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "id",
        "title",
        # "is_active",
        # "is_deleted",
        # "created_at",
        # "updated_at",
        "student",
        "start_time",
        "end_time",
        "room",
        "attendence",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "student"]
    list_filter = ["event"]
