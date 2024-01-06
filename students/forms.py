import re
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm
from students.models import Student


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
    
    def clean_name(self):
        print("clean_name")
        name = self.cleaned_data.get('name')
        if self.instance and self.instance.pk:
            # Editing an existing student
            if Student.objects.filter(Q(name__iexact=name) & ~Q(pk=self.instance.pk)).exists():
                raise ValidationError("Student with name %(name)s already exists." % {"name": name})
        else:
            # Creating a new student
            if Student.objects.filter(name__iexact=name).exists():
                raise ValidationError("Student with name %(name)s already exists." % {"name": name})
        return name
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^[0-9+\- ]+$', phone):
            raise ValidationError(
                "Phone number can only contain digits (0-9), plus sign (+), hyphen (-), and space ( )")
        return phone

