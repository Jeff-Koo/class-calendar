from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

import calendar
from datetime import datetime
from calendarapp.models import Event

weekday_names = list(calendar.day_abbr)

class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        all_events = Event.objects.get_all_events()
        future_events = Event.objects.get_future_events()
        running_events = Event.objects.get_running_events()
        latest_events = Event.objects.filter().order_by("-id")[:10]

        now = datetime.now()
        all_events_with_dates = []
        for event in all_events:
            event_date = event.start_time.date()
            event_start_time = event.start_time.time()
            event_end_time = event.end_time.time()
            
            event_color = "" # default none
            if event.start_time < now:
                if event.attendence:
                    event_color = "#2ec285" # green
                else:
                    event_color = "#ff6b6b" # red
            
            event_dict = {
                "event": event,
                "event_date": event_date.strftime("%d/%m/%Y"),
                "event_date_weekday": weekday_names[event_date.weekday()], 
                "event_start_time": event_start_time.strftime("%I:%M %p"),
                "event_end_time": event_end_time.strftime("%I:%M %p"),
                "event_color": event_color,
            }
            all_events_with_dates.append(event_dict)
        
        future_events_with_dates = []
        for event in future_events:
            event_date = event.start_time.date()
            event_start_time = event.start_time.time()
            event_end_time = event.end_time.time()
            
            event_color = "" # default none
            if event.start_time < now:
                if event.attendence:
                    event_color = "#2ec285" # green
                else:
                    event_color = "#ff6b6b" # red
            
            event_dict = {
                "event": event,
                "event_date": event_date.strftime("%d/%m/%Y"),
                "event_date_weekday": weekday_names[event_date.weekday()], 
                "event_start_time": event_start_time.strftime("%I:%M %p"),
                "event_end_time": event_end_time.strftime("%I:%M %p"),
                "event_color": event_color,
            }
            future_events_with_dates.append(event_dict)

        
        
        context = {
            "total_event": all_events.count(),
            # "all_events": all_events,
            # "future_events": future_events,
            # "running_events": running_events,
            # "latest_events": latest_events,
            "all_events_with_dates": all_events_with_dates,
            "future_events_with_dates": future_events_with_dates,
        }
        return render(request, self.template_name, context)
