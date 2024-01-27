# cal/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from calendarapp.models import EventMember, Event
from students.models import Student
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm, InputMemberToEventForm
from django.contrib import messages
from django.utils.html import strip_tags
from django.db import transaction


weekday_names = list(calendar.day_abbr)

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def get_event_color(event):
    now = datetime.now()
    event_color = "#3788d8" # default blue
    if event.start_time < now:
        if event.attendence:
            event_color = "#2ec285" # green
        else:
            event_color = "#ff6b6b" # red
    return event_color


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signin")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signin")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                student = forms.cleaned_data["student"]
                EventMember.objects.create(event=event, student=student)
                return redirect("calendarapp:calendar")
            else:
                print("--------------Student limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events()
        events_today = Event.objects.get_today_events()
        event_list = []
        for event in events:
            event_color = get_event_color(event)
            event_list.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": event.description,
                    "room": "Room " + event.room,
                    "event_color": event_color,
                    "student": event.student.name,
                    "attendence": 1 if event.attendence else 0,
                    # more data for eventContent in calendar
                    "resourceId": event.room,
                    "backgroundColor": event_color,
                }
            )
        
        context = {
            "form": forms, 
            "events": event_list,
            "events_today": events_today,
            "scheduler_license_key": settings.SCHEDULER_LICENSE_KEY,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            start_time = forms.cleaned_data["start_time"]
            end_time = forms.cleaned_data["end_time"]
            room = forms.cleaned_data['room']
            student_input = forms.cleaned_data['student']
            student, student_created = Student.objects.get_or_create(
                name=student_input,
            )
            start_timeonly_str = start_time.strftime("%H:%M")
            
            try:
                Event.objects.create(
                    title = f"{student.name} - {start_timeonly_str} (Room {room}) ",  # Update the title field,
                    description = "nothing",
                    start_time=start_time,
                    end_time=end_time,
                    student=student,
                    room=room,
                )
            except:
                messages.error(request, 'the same Student is already in the same Class!')
                return redirect("calendarapp:calendar")
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)


def toggle_attendence(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        current_attendence = event.attendence
        event.attendence = not event.attendence
        event.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event success delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def edit_event(request, event_id):
    """ mainly handle drag drop event """
    parsed_body = request.POST.dict()
    # print("parsed_body:", parsed_body)
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        # change the time base on the drag and drop
        event.start_time = parsed_body['start']
        event.end_time = parsed_body['end']
        event.room = parsed_body['room']
        event.attendence = parsed_body['attendence']
        
        # update the title
        start_datetime_obj = datetime.strptime(event.start_time, "%Y-%m-%d %H:%M:%S")
        start_timeonly_str = start_datetime_obj.strftime("%H:%M")
        event.title = f"{event.student.name} - {start_timeonly_str} (Room {event.room}) "
        event.description = "nothing"
        try:
            event.save()
            return JsonResponse({'message': 'Event success moved.'})
        except:
            return JsonResponse({'message': 'Same person in Same timeslot!'}, status=400)
    else:
        return JsonResponse({'message': 'Error: Something Wrong. Try Again Later'}, status=400)

def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def multi_input_member_to_event(request):
    
    if request.method == 'POST':

        form = InputMemberToEventForm(request.POST)
        
        errors = form.errors.as_data()
        formatted_errors = {}
        for field, error_list in errors.items():
            formatted_errors[field] = strip_tags(str(error_list[0]))[2:-2]
        error_message = str("<br>".join(formatted_errors.values()))
        messages.error(request, mark_safe(error_message))
        
        if form.is_valid():
            student_input = form.cleaned_data['student']
            listOfDate = form.cleaned_data['listOfDate']
            timeslots = [
                form.cleaned_data['timeslot0'],  # Monday
                form.cleaned_data['timeslot1'],  # Tuesday
                form.cleaned_data['timeslot2'],  # Wednesday
                form.cleaned_data['timeslot3'],  # Thursday
                form.cleaned_data['timeslot4'],  # Friday
                form.cleaned_data['timeslot5'],  # Saturday
                form.cleaned_data['timeslot6'],  # Sunday
            ]
            room = form.cleaned_data['room']
            
            # create student if not exists
            student, student_created = Student.objects.get_or_create(
                name=student_input,
            )
            
            
            arrayOfDate = listOfDate.splitlines()
            arrayOfDate = [date.strip() for date in arrayOfDate if date.strip()]
            
            arrayOfFormattedDate = []
            for date in arrayOfDate:
                try:
                    # format the date strings
                    arrayOfFormattedDate.append(datetime.strptime(date, '%Y/%m/%d').date())
                except:
                    messages.error(request, 'something wrong with the input date!')
                    form = InputMemberToEventForm(
                        initial={
                            'student': student_input,
                            'room': room,
                            'listOfDate': listOfDate,
                            'timeslot0': timeslots[0],
                            'timeslot1': timeslots[1],
                            'timeslot2': timeslots[2],
                            'timeslot3': timeslots[3],
                            'timeslot4': timeslots[4],
                            'timeslot5': timeslots[5],
                            'timeslot6': timeslots[6],
                        }
                    )
                    return render(request, 'calendarapp/input_event_member.html', {'form': form})
            
            
            arrayOfFormattedEvents = []

            for date in arrayOfFormattedDate:
                
                # get weekday of each date
                weekday = date.weekday()
                
                # Get the corresponding timeslot variable based on the weekday
                timeslot_value = timeslots[weekday]
                
                # split timeslot , may trigger error for the default empty choice
                # may check in frontend, without storing any entry in database
                try:
                    start_timeonly_str, end_timeonly_str = timeslot_value.split(' ~ ')
                except:
                    messages.error(request, f'Missing input for {date} ({weekday_names[weekday]})')
                    form = InputMemberToEventForm(
                        initial={
                            'student': student_input,
                            'room': room,
                            'listOfDate': listOfDate,
                            'timeslot0': timeslots[0],
                            'timeslot1': timeslots[1],
                            'timeslot2': timeslots[2],
                            'timeslot3': timeslots[3],
                            'timeslot4': timeslots[4],
                            'timeslot5': timeslots[5],
                            'timeslot6': timeslots[6],
                        }
                    )
                    return render(request, 'calendarapp/input_event_member.html', {'form': form})
                
                # format the time string
                start_timeonly = datetime.strptime(start_timeonly_str, '%H:%M').time()
                end_timeonly = datetime.strptime(end_timeonly_str, '%H:%M').time()
                
                # Combine the date and time into a datetime object
                start_time = datetime.combine(date, start_timeonly)
                end_time = datetime.combine(date, end_timeonly)
                
                # Format the combined datetime as a string
                formatted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%S')
                formatted_end_time = end_time.strftime('%Y-%m-%dT%H:%M:%S')
                
                arrayOfFormattedEvents.append({
                    'start_time': formatted_start_time,
                    'end_time': formatted_end_time,
                    'title': f"{student.name} - {start_timeonly_str} (Room {room}) ",  # Update the title field
                })
                
            # create the lesson if not exist
            try:
                with transaction.atomic():
                    for formattedEvent in arrayOfFormattedEvents:
                        event = Event.objects.create(
                            start_time = formattedEvent['start_time'],
                            end_time = formattedEvent['end_time'],
                            room = room,
                            student = student,
                            title = formattedEvent['title'],
                            description = "nothing",
                            attendence = False,
                        )
            except:
                messages.error(request, 'the same Student is already in the same Class!')
                form = InputMemberToEventForm(
                    initial={
                        'student': student_input,
                        'room': room,
                        'listOfDate': listOfDate,
                        'timeslot0': timeslots[0],
                        'timeslot1': timeslots[1],
                        'timeslot2': timeslots[2],
                        'timeslot3': timeslots[3],
                        'timeslot4': timeslots[4],
                        'timeslot5': timeslots[5],
                        'timeslot6': timeslots[6],
                    }
                )
                return render(request, 'calendarapp/input_event_member.html', {'form': form})
                
                # try to add the student to the lesson 
                # try:
                #     EventMember.objects.create(event = event, student = student)
                # except:
                #     messages.error(request, 'the same Student is already in the same Class!')
                #     form = InputMemberToEventForm(
                #         initial={
                #             'student': student_input,
                #             'room': room,
                #             'listOfDate': listOfDate,
                #             'timeslot': timeslot,
                #         }
                #     )
                #     return render(request, 'calendarapp/input_event_member.html', {'form': form})
            
            messages.success(request, 'Success!')
            return redirect('calendarapp:calendar')
    else:
        form = InputMemberToEventForm()

    return render(request, 'calendarapp/input_event_member.html', {'form': form})

