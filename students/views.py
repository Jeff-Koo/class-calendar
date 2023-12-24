from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from students.models import Student



@login_required
def all_student(request: HttpRequest) -> HttpResponse:

    student_list = Student.objects.all()
    
    context = { 
        'student_list' : student_list, 
    }
    
    # return render(request, 'ai_tools/ai_home.html', context)
    return request


# view student detail with attendence on his/her lessons
@login_required
def get_student(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        print("wrong, not such student")
        # return redirect('ai_home')

    # context = { 
    #     'student' : student,
    # }
    
    # return render(request, 'ai_tools/ai_detail.html', context)
    return request

