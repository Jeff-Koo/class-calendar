from django.forms import ModelForm
from students.models import Student
from django import forms


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["name", "phone", "memo"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Student Name"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Optional: Enter Phone Number"}
            ),
            "memo": forms.Textarea(
                attrs={"class": "form-control"}
            ),
        }
