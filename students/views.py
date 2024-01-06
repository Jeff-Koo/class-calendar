from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

import calendar
from students.models import Student
from calendarapp.models import Event


weekday_names = list(calendar.day_abbr)

@login_required(login_url="signup")
def all_student(request: HttpRequest) -> HttpResponse:
    student_list = Student.objects.all()
    context = { 
        'student_list' : student_list, 
    }
    return render(request, 'students/students_list.html', context)


# view student detail with attendence on his/her lessons
@login_required(login_url="signup")
def get_student(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        print("wrong, not such student")
        return redirect('all_student')
    
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
        }
        events_with_dates.append(event_dict)

    context = { 
        'student' : student,
        'event_list' : events_with_dates,
    }
    
    return render(request, 'students/students_detail.html', context)

