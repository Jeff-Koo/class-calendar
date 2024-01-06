from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

import calendar
from students.forms import StudentForm
from students.models import Student
from calendarapp.models import Event


weekday_names = list(calendar.day_abbr)

def get_event_color_student_detail(event):
    now = datetime.now()
    event_color = "" # default none
    if event.start_time < now:
        if event.attendence:
            event_color = "#2ec285" # green
        else:
            event_color = "#ff6b6b" # red
    return event_color

@login_required(login_url="signup")
def all_student(request: HttpRequest) -> HttpResponse:
    student_list = Student.objects.all()
    form_student = StudentForm
    context = { 
        'form_student': form_student,
        'student_list': student_list, 
    }
    return render(request, 'students/students_list.html', context)


# view student detail with attendence on his/her lessons
@login_required(login_url="signup")
def get_student(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        messages.error(request, 'Something wrong! No such Student')
        return redirect('all_student')
    
    form_student = StudentForm
    form_edit = StudentForm(instance = student)
    event_list = Event.objects.filter(student=student)
    events_with_dates = []
    for event in event_list:
        # I want to get teh date from event.start_time
        event_date = event.start_time.date()
        event_start_time = event.start_time.time()
        event_end_time = event.end_time.time()
        event_dict = {
            "event": event,
            "event_date": event_date.strftime("%d/%m/%Y"),
            "event_date_weekday": weekday_names[event_date.weekday()], 
            "event_start_time": event_start_time.strftime("%I:%M %p"),
            "event_end_time": event_end_time.strftime("%I:%M %p"),
            "event_color": get_event_color_student_detail(event),
        }
        events_with_dates.append(event_dict)

    context = { 
        'form_student': form_student,
        'form_edit': form_edit,
        'student': student,
        'event_list': events_with_dates,
    }
    
    return render(request, 'students/students_detail.html', context)


@login_required(login_url="signup")
def add_student(request: HttpRequest):
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Add Student Success!')
            return redirect('all_student')
        else:
            messages.error(request, 'Error: Maybe there is student has the same name!')
            return redirect('all_student')
    else:
        messages.error(request, 'Something wrong!')
        return redirect('all_student')


@login_required(login_url="signup")
def edit_student(request: HttpRequest, pk: int):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        messages.error(request, 'Something wrong! No such Student')
        return redirect('all_student')
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance = student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Student Info Success!')
            return redirect('get_student', pk=pk)
        else:
            messages.error(request, 'Error: Maybe there is student has the same name!')
            return redirect('get_student', pk=pk)
    else:
        messages.error(request, 'Something wrong!')
        return redirect('get_student', pk=pk)

