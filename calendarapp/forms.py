from django.forms import ModelForm, DateInput, ValidationError
from calendarapp.models import Event, EventMember
from students.models import Student
from django import forms
from django_select2 import forms as s2forms


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["room"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["student"]


TIMESLOT_CHOICES = (
    ('09:00 ~ 10:00', '09:00 ~ 10:00 for Mon to Fri / 09:30 ~ 10:30 for Sat'),
    ('10:00 ~ 11:00', '10:00 ~ 11:00 for Mon to Fri / 10:30 ~ 11:30 for Sat'),
    ('11:00 ~ 12:00', '11:00 ~ 12:00 for Mon to Fri / 11:30 ~ 12:30 for Sat'),
    ('13:00 ~ 14:00', '13:00 ~ 14:00'),
    ('14:00 ~ 15:00', '14:00 ~ 15:00'),
    ('15:00 ~ 16:00', '15:00 ~ 16:00'),
    ('16:00 ~ 17:00', '16:00 ~ 17:00'),
    ('17:00 ~ 18:00', '17:00 ~ 18:00'),
    ('18:00 ~ 19:00', '18:00 ~ 19:00'),
)

ROOM_CHOICES = (
    ('A', 'Room A'),
    ('B', 'Room B'),
    ('C', 'Room C'),
)

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
            'placeholder': 'e.g.\n2023/12/01\n2023/12/8\n2023/12/15', 
            'rows': 20, 
        }),
        required=True
    )
    timeslot = forms.ChoiceField(
        label='Start Time to End time', 
        choices=TIMESLOT_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    room = forms.ChoiceField(
        label='Room', 
        choices=ROOM_CHOICES, 
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    def clean_listOfDate(self):
        try:
            listOfDate = self.cleaned_data.get('listOfDate')
            arrayOfDate = listOfDate.splitlines()
            arrayOfDate = [date.strip() for date in arrayOfDate if date.strip()]

            print("\nafter date.strip():", arrayOfDate)
            return arrayOfDate
        except:
            raise ValidationError("Please enter the valid dates.")

