from datetime import datetime
from django.db import models
from django.urls import reverse

from calendarapp.models import EventAbstract
from accounts.models import User
from students.models import Student


class TIMESLOT_CHOICES(models.TextChoices):
    NINE = '09:00 ~ 10:00', '09:00 ~ 10:00 for Mon to Fri / 09:30 ~ 10:30 for Sat'
    TEN = '10:00 ~ 11:00', '10:00 ~ 11:00 for Mon to Fri / 10:30 ~ 11:30 for Sat'
    ELEVEN = '11:00 ~ 12:00', '11:00 ~ 12:00 for Mon to Fri / 11:30 ~ 12:30 for Sat'
    THIRTEEN = '13:00 ~ 14:00', '13:00 ~ 14:00'
    FOURTEEN = '14:00 ~ 15:00', '14:00 ~ 15:00'
    FIFTEEN = '15:00 ~ 16:00', '15:00 ~ 16:00'
    SIXTEEN = '16:00 ~ 17:00', '16:00 ~ 17:00'
    SEVENTEEN = '17:00 ~ 18:00', '17:00 ~ 18:00'
    EIGHTEEN = '18:00 ~ 19:00', '18:00 ~ 19:00'


class ROOM_CHOICES(models.TextChoices):
    ROOM_A = 'Room A', 'Room A'
    ROOM_B = 'Room B', 'Room B'
    ROOM_C = 'Room C', 'Room C'


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


class Event(EventAbstract):
    """ Event model """

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_event", null=True)
    room = models.TextField(choices=ROOM_CHOICES.choices, blank=True)

    objects = EventManager()

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

