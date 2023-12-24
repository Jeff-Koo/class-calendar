from django.db import models

from students.models import Student
from calendarapp.models import Event, EventAbstract


class EventMember(models.Model):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="event_members")
    attendence = models.BooleanField(default=False)

    class Meta:
        unique_together = ["event", "student"]

    def __str__(self):
        return str(self.student)
