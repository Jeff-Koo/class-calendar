from datetime import datetime, time
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from calendarapp.models import EventAbstract
from students.models import Student


class ROOM_CHOICES(models.TextChoices):
    ROOM_A = 'A', 'Room A'
    ROOM_B = 'B', 'Room B'
    ROOM_C = 'C', 'Room C'
    ROOM_OFF = 'OFF', 'OFF'


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self):
        events = Event.objects.filter(is_active=True, is_deleted=False)
        return events

    def get_running_events(self):
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

    def get_future_events(self):
        start_of_today = datetime.combine(datetime.today(), time(0, 0, 0, 0))
        
        future_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            start_time__gte=start_of_today,
        ).order_by("start_time")
        return future_events

    def get_today_events(self):
        start_of_today = datetime.combine(datetime.today(), time(0, 0, 0, 0))
        end_of_today = datetime.combine(datetime.today(), time(23, 59, 59, 999999))
        
        today_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            start_time__gte=start_of_today,
            end_time__lte=end_of_today,
        ).order_by("start_time")
        return today_events


class Event(EventAbstract):
    """ Event model """

    title = models.CharField(max_length=200)
    description = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_class")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    room = models.TextField(choices=ROOM_CHOICES.choices, blank=True)
    attendence = models.BooleanField(default=False)

    objects = EventManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['student', 'start_time', 'end_time'],
                name='unique_student_timeslot'
            )
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def admin_url(self) -> str:
        return reverse('admin:calendarapp_event_change', args=[self.pk])

