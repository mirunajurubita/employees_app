from pyexpat.errors import messages
from time import time
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from urllib3 import HTTPResponse
from .models import User, Tasks, Report, Attendance, Pause
from .forms import EmployeeSignUpForm
from django.views.generic import CreateView
from django.db.models import F
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum
import numpy as np
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from.filters import EmployeeReporsFilterForm, EmployeeAttendanceFilterForm
from datetime import datetime, timedelta, time, date


#@login_required()
def employee_page(request):

    return render(request, "employee_page.html")
    
class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'register_employee.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('loginUser')



#@login_required()
def viewActiveTasks(request):
    current_user = request.user
    current_user_id = current_user.id
    tasks = Tasks.objects.filter(user_id = request.user.id)
    #pauses = Pause.objects.filter(user_id = request.user.id)
    return render(request, "employees_active_tasks.html", {'tasks':tasks})

def endTask(request, id):

    task = Tasks.objects.get(id=id)
    user_employees = User.objects.filter(is_employee=1, id = request.user.id)
    attendance = Attendance.objects.filter(user_id = request.user.id).last()
    print(attendance)

    if task.is_active == 1:
        task.is_active = 0    
    task.closed_at = timezone.now()

    if task.closed_at > task.deadline:
        task.is_overdue=1

    diff = abs(task.started_at - task.closed_at)

    
    if task.closed_at.date() == task.started_at.date():
        time_of_work = int(diff.total_seconds()/60)*60
        print("time_of_work")
        print(time_of_work)
        task.task_time = timedelta(seconds=time_of_work)/1000000
        print(task.task_time)
    else:


        if task.closed_at.day - task.started_at.day == 1:
            attendance1 = Attendance.objects.get(start_time__date = task.started_at.date())
            attendance2 = Attendance.objects.get(start_time__date = timezone.now().date())
            #time_of_work = diff.total_seconds() / 3600.00 - 16.00
            time_of_work = diff.total_seconds() - (attendance2.start_time-attendance1.end_time).total_seconds()
            print((attendance2.start_time-attendance1.end_time).total_seconds())
            print("DIFF TOTAL SEC")
            print(diff.total_seconds())
            print("TIME OF WORK")
            print(time_of_work)
            """
            #task.days = 0
            task.hours = int(time_of_work)
            task.minutes = int((time_of_work - task.hours) * 60)
            task.seconds = int(((time_of_work - task.hours) * 60 - task.minutes)*60)
            """
            #task.task_time = str(datetime.timedelta(seconds=time_of_work))
            task.task_time = timedelta(seconds=time_of_work)/1000000 
            
        #altfel daca task-ul e poimaine au mai mult
        elif task.closed_at.day - task.started_at.day > 1 or task.closed_at.month!=task.started_at.month:
            closed_at_date = task.closed_at.date()
            assigned_at_date = task.started_at.date()
            total_days = task.closed_at.day - task.assigned_at.day +1
            weekend_days = np.busday_count(assigned_at_date, closed_at_date, weekmask='0000011')

            l = []
            attendances = Attendance.objects.filter(user_id = request.user.id)
            for i in range(0, len(attendances)-1):
                if attendances[i].start_time <= timezone.now():
                        time_of_work = diff.total_seconds() - (attendance[i+1].start_time-attendance[i].end_time).total_seconds()
            closed_at_date = task.closed_at.date()
            assigned_at_date = task.started_at.date()
            weekend_days = np.busday_count(assigned_at_date, closed_at_date, weekmask='0000011')
            time_of_work = time_of_work - 24*weekend_days*3600

            task.task_time = timedelta(seconds=time_of_work)/1000000

    task.task_effective_time = timedelta(seconds = (task.task_time.total_seconds())) - task.pause_time


            
            #task.task_time = str(datetime.timedelta(seconds=time_of_work))
    task.task_time = timedelta(seconds=time_of_work)/1000000
    """
    count = 0
    tasks = Tasks.objects.filter(user_id = request.user.id)
    #daca gaseste task activ face is_busy = 1
    for i in tasks:
        if i.is_active == 1:
            count +=1

    print(type(task.task_time))
    print(type(task.pause_time))
    if task.start_pause_date == task.finish_pause_date:
        time_str = "00:00:00"
        time_format = "%H:%M:%S"
        parsed_time = datetime.strptime(time_str, time_format).time()
        task.pause_time = parsed_time

    """
    #pause = Pause.objects.filter(task_id = task.id)
    #pauses_time = Pause.objects.filter(task_id = task.id).aaggregate(Sum('pause_time'))
    #print(pauses_time)
    #print(pause)
    
    task.task_effective_time = timedelta(seconds = (task.task_time.total_seconds())) - task.pause_time
    print(task.task_effective_time)
    
    #task.task_effective_time = str(datetime.combine(datetime.today(), datetime.strptime(task.task_time, "%H:%M:%S").time())  - datetime.combine(datetime.today(), task.pause_time))

    task.is_completed = 1
    task.save()
    #print(time_of_work)
    
    #time_in_seconds = datetime.timedelta(seconds=time_of_work).seconds
    hours = int(time_of_work / 3600)
    minutes = int(((time_of_work / 3600) - int(time_of_work / 3600))*60)

    my_tasks = Tasks.objects.filter(user_id = request.user.id, is_active = 1)
    count1 = 0
    #numar sa vad daca am task uri active la momentul cand inchid taskul 
    for i in my_tasks:
        #if i.is_active == 1 and i.id !=id:
        if i.id !=id:
            count1 +=1
    reports = Report.objects.filter(user_id = request.user.id)
    count2 =  0
    for i in reports:
        if i.current_date.date() == timezone.now().date():
            count2 +=1
    if count1 == 0 and count2 == 0:
        report = Report( 
                        user_id = User.objects.get(id = request.user.id), 
                        current_date = timezone.now(), 
                        completed_tasks = 0, 
                        uncompleted_tasks = 0,
                        r_type = "Daily",
                        work_time = timedelta(seconds = 0 ),
                        pause_time = timedelta(seconds = 0 )
                        )
        report.save()
    return render(request, "employees_end_tasks.html", {"task":  task,  "user_employees":  user_employees, "hours":hours,
            "minutes":minutes})
    #return render(request, "employees_eactive_tasks.html")

#return render(request, 'employees_end_tasks.html')

def employeeClosedTasks(request):
    user_employee = request.user
    tasks = Tasks.objects.filter(user_id = request.user.id).order_by('-closed_at')
    return render(request, 'employee_closed_tasks.html',{"tasks":tasks,"user_employee": user_employee})

def viewMyReports(request):
    print(request.user.id)
    reports = Report.objects.filter(user_id = request.user.id)
    if request.method == 'POST':
        form = EmployeeReporsFilterForm(request.POST)
        if form.is_valid():
            column = form.cleaned_data['column']
            value = form.cleaned_data['value']
            reports = Report.objects.filter(**{column: value})

    else:
        form = EmployeeReporsFilterForm()
    return render(request, 'employee_myreports.html',{"reports": reports,"form":form})

def viewReport(request,pk): 
    report = Report.objects.get(id = pk)
    r_date = report.current_date.date()
    print(report.id)
    #daily
    tasks = report.tasks.all()
    pauses = Pause.objects.all()

    #weekly
    #monthly
    #annual
    return render(request, 'view_report.html',{"report":report,"tasks":tasks,"pauses":pauses})

def startTask(request, id):
    #employees=Employee.objects.(user_id=request.user.id)
    task = Tasks.objects.get(id=id)
    user_employees = User.objects.filter(is_employee=1, id = request.user.id)
    tasks = Tasks.objects.filter(user_id = task.user_id)
    #employees.active_tasks = employees.active_tasks +1
    task.started_at = timezone.now()
    task.is_active = 1
    task.save()
    #employees.is_busy = 1
    #employees.save()
    #pun stop la pauza
    #imi aleg toate task urile mele
    my_tasks = Tasks.objects.filter(user_id = request.user.id)
    count = 0
    for task in my_tasks:
        if task.is_active == 1 and task.id !=id:
            count +=1
    print("count")
    print(count)
    try:
        rep = Report.objects.get(current_date__date = timezone.now().date())
    except Report.DoesNotExist:
        rep = None
    print(rep)
    #daca nu am rapoarte si nu am task uri active    
    if not rep and count == 0:
        report = Report( 
                        user_id = User.objects.get(id = request.user.id), 
                        current_date = timezone.now(), 
                        completed_tasks = 0, 
                        uncompleted_tasks = 0,
                        r_type = "Daily",
                        work_time = timedelta(seconds = 0 ),
                        pause_time = timedelta(seconds = 0 )
                        )
        report.save()
    else:
        if count == 0:
            report = Report.objects.get(current_date__date = timezone.now().date())
            print(timezone.now().time())
            report.pause_time = datetime.combine(datetime.today(), datetime.strptime(str(timezone.now().time().strftime("%H:%M:%S")), "%H:%M:%S").time())  - datetime.combine(datetime.today(), report.current_date.time())

            report.current_date = timezone.now()
            report.save()

    #daca count e 0 inseamna ca nu am task uri active deci nu incep nicio pauza
    """
    if count == 0:
        pauses = Pause.objects.filter(user_id = task.user_id)
        for pause in pauses:
            if pause.start_pause_date == pause.finish_pause_date:
                pause.finish_pause_date = timezone.now()
                pause.save()
"""

    return render(request, "employees_active_tasks.html", {"user_employees":  user_employees,"tasks":tasks})
"""
def startPause(request, pk):
    #employee = Employee.objects.get(user_id = request.user.id)
    print(datetime.datetime.now())
    pause = Pause(user_id =User.objects.get(id = request.user.id), start_pause_date = timezone.now(),finish_pause_date = timezone.now(), task_id = pk)
    pause.save()
    #return render(request,"employee_page.html")

    return render(request, "employees_start_pause.html")

"""

def editTask(request, id):
    task = Tasks.objects.get(id = id)
    return render(request,"employees_edit_pause.html", {"id":id})

def editTaskSave(request, id):
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        location=request.POST.get("location")
        pause_details=request.POST.get("pause_details")
        task_id = id 
        print(task_id)
        pause = Pause.objects.create(task_id = Tasks.objects.get(id = task_id), location = location, pause_details = pause_details, start_pause_date = timezone.now())
        """
        pause.location = location
        pause.pause_details =  pause_details
        pause.start_pause_date = timezone.now()
        """
        pause.save()
        return redirect("viewActiveTasks")

def endPause(request, id):
    pause = Pause.objects.filter(task_id = id).order_by('-start_pause_date').first()
    print(pause)
    pause.finish_pause_date = timezone.now()
    
    pause.pause_time = pause.pause_time + timedelta(seconds= (pause.finish_pause_date- pause.start_pause_date).total_seconds()/1000000)
    task = Tasks.objects.get(id = id)
    report = Report.objects.get(user_id = task.user_id,current_date__date = timezone.now().date())

    #t1 = datetime.combine(date.min, report.pause_time) - datetime.min
    s = report.pause_time.total_seconds()+pause.pause_time.total_seconds()
    print("total seconds pause time")
    print(pause.pause_time.total_seconds())
    print("treport.pause_time")
    print(report.pause_time.total_seconds())

    report.pause_time = timedelta(seconds = s)
    task.pause_time += pause.pause_time
    print(report.pause_time)
    print(type(s))
    print(pause.finish_pause_date)
    pause.save()
    report.save()
    task.save()
    return redirect("viewActiveTasks")

def onlyEdit(request,id):
    task = Tasks.objects.get(id = id)
    print(task)
    return render(request,"employees_edit_save.html", {"id":id})


def onlyEditSave(request, id):
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        location=request.POST.get("location")
        pause_details=request.POST.get("pause_details")
        task_id = id 
        print(task_id)
        task = Tasks.objects.get(id = task_id)
        task.location = location
        task.pause_details =  pause_details
        task.save()
        return redirect("employeeClosedTasks")

def viewAttendance(request):
    schedules = Attendance.objects.filter(user_id = request.user.id).order_by("-start_time")
    if request.method == 'POST':
        form = EmployeeAttendanceFilterForm(request.POST)
        if form.is_valid():
            column = form.cleaned_data['column']
            value = form.cleaned_data['value']
            schedules = Attendance.objects.filter(**{column: value})

    else:
        form = EmployeeAttendanceFilterForm()
    return render(request, "employee_view_attendance.html",{"schedules":schedules,"form":form})

def editAttendance(request):
    attendance = Attendance.objects.filter(user_id = request.user.id,).last()
    attendance_id = attendance.id
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        end_time=request.POST.get("end_time")
        attendance = Attendance.objects.get(id = attendance_id)
        attendance.end_time = end_time
        attendance.save()
    return redirect("viewAttendance")