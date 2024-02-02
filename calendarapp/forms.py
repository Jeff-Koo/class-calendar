from django.forms import ModelForm, DateInput, ValidationError
from calendarapp.models import Event, EventMember
from students.models import Student
from django import forms
from django_select2 import forms as s2forms


TIMESLOT_CHOICES = (
    ('-------------', '-------------'),
    ('09:00 ~ 10:00', '09:00 ~ 10:00'),
    ('09:30 ~ 10:30', '09:30 ~ 10:30'),
    ('10:00 ~ 11:00', '10:00 ~ 11:00'),
    ('10:30 ~ 11:30', '10:30 ~ 11:30'),
    ('11:00 ~ 12:00', '11:00 ~ 12:00'),
    ('11:30 ~ 12:30', '11:30 ~ 12:30'),
    ('13:00 ~ 14:00', '13:00 ~ 14:00'),
    ('13:30 ~ 14:30', '13:30 ~ 14:30'),
    ('14:00 ~ 15:00', '14:00 ~ 15:00'),
    ('14:30 ~ 15:30', '14:30 ~ 15:30'),
    ('15:00 ~ 16:00', '15:00 ~ 16:00'),
    ('15:30 ~ 16:30', '15:30 ~ 16:30'),
    ('16:00 ~ 17:00', '16:00 ~ 17:00'),
    ('16:30 ~ 17:30', '16:30 ~ 17:30'),
    ('17:00 ~ 18:00', '17:00 ~ 18:00'),
    ('17:30 ~ 18:30', '17:30 ~ 18:30'),
    ('18:00 ~ 19:00', '18:00 ~ 19:00'),
)

ROOM_CHOICES = (
    ('A', 'Room A'),
    ('B', 'Room B'),
    ('C', 'Room C'),
)


class EventForm(forms.Form):
    student = forms.ModelChoiceField(
        label='Student Name', 
        queryset=Student.objects.all(),
        widget=s2forms.Select2Widget(
            attrs={'style': 'width: 100%;'}
        ),
    )
    start_time = forms.DateTimeField(
        widget=DateInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
    )
    end_time = forms.DateTimeField(
        widget=DateInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
    )
    room = forms.ChoiceField(
        label='Room', 
        choices=ROOM_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["student"]


class InputMemberToEventForm(forms.Form):
    student = forms.ModelChoiceField(
        label='Student Name', 
        queryset=Student.objects.all(),
        widget=s2forms.Select2Widget(
            attrs={'style': 'width: 100%;'}
        ),
    )
    listOfDate = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control border-radius-0 mb-2', 
            'placeholder': 'e.g.\n2023/12/1\n2023/12/15\n2024/1/1', 
            'rows': 20, 
        }),
        required=True
    )
    timeslot0 = forms.ChoiceField(
        label='Start Time to End time for Monday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot1 = forms.ChoiceField(
        label='Start Time to End time for Tuesday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot2 = forms.ChoiceField(
        label='Start Time to End time for Wednesday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot3 = forms.ChoiceField(
        label='Start Time to End time for Thursday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot4 = forms.ChoiceField(
        label='Start Time to End time for Friday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot5 = forms.ChoiceField(
        label='Start Time to End time for Saturday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    timeslot6 = forms.ChoiceField(
        label='Start Time to End time for Sunday', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    room = forms.ChoiceField(
        label='Room', 
        choices=ROOM_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

