from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from urllib3 import HTTPResponse
from .forms import ManagerSignUpForm, EmployeeSignUpForm
from .models import  User, Tasks, Report, Attendance, Pause
from django.http import  HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.utils import timezone
import calendar
from calendar import HTMLCalendar
from django.contrib.messages.views import SuccessMessageMixin
import requests
from django.http import JsonResponse
from django.db.models import Avg, Max, Min
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from pyfcm import FCMNotification
import dateutil.parser
from datetime import datetime, timedelta, time, date 
import numpy as np
import calendar
from django.core.mail import send_mail
from.filters import TaskFilterForm,ClosedTaskFilterForm
from django.contrib import messages
from django.template.defaultfilters import timesince 
from django import template
from dateutil.rrule import rrule, DAILY

#@login_required()
def manager_page(request):
    return render(request, "manager_page.html")


class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'register_manager.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('loginUser')

class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'register_employee.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        print(user)
        #login(self.request, user)
        return redirect('managerPage')




def addTask(request):
    employees =  User.objects.filter(is_employee=1)
    
    #deadline = timezone.now() , "deadline_pick": deadline
    return render(request,"add_task.html", {'employees': employees })
#@login_required()


def send_notification_to_flutter(fcm_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body

        ),
        token=fcm_token
    )
    response = messaging.send(message)
    return response


def addTaskSave(request):
    l = []
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        l = request.POST.getlist("usernames")
        print(l)
        headline=request.POST.get("headline")
        body=request.POST.get("body")
        deadline = request.POST.get("deadline")
        task_type = request.POST.get("task_type")
        print(headline)
        print(body)
        
        print(deadline)
        #assigned_at =request.POST.get("assigned_at")
        for i in l:
            user = User.objects.get(username = i)
            print(type(user))
            try:
                task_model=Tasks(headline=headline, body = body, deadline = deadline, user_id = user,task_type = task_type)
                
                task_model.author = request.user
                print(task_type)
                task_model.save()
                print("task saved")
                print("user id")
                print(user.id)
                print(task_model)
                #messages.success(request, "Task added successfully!")
                #METODA 1
                device = FCMDevice.objects.get(user_id = user.id, active=1)
                DEVICE_TOKEN = device.registration_id
                print("device token e")
                print(DEVICE_TOKEN)
                """
                    # Initialize the FCMNotification object with your API key
                    push_service = FCMNotification(api_key="")

                    # Set the notification data
                    message_title = "Uber update"
                    message_body = "Hi john, your customized news for today is ready"
                    # Set the list of registration tokens for the devices that you want to send the notification to

                    # Send the notification
                    result = push_service.notify_single_device(registration_id=DEVICE_TOKEN, message_title=message_title, message_body=message_body)            
                    print("result e")
                    print(result)
                """
                d = dateutil.parser.parse(task_model.deadline)
                    #METODA 2
                FCM_ENDPOINT = 'https://fcm.googleapis.com/fcm/send'
                FCM_API_KEY = ''
                payload = {
                        "to": DEVICE_TOKEN,
                        "notification": {
                            "title": task_model.headline,
                            "body": "Deadline : {} {}  Status: {}".format(d.strftime('%m/%d/%Y'),d.strftime("%H:%M"),task_model.task_type) 
                        },
                        "android": {
                            "priority": "high"
                        }
                        }
                print("PAYLOAD")
                print(payload)
                headers = {
                        'Authorization': 'key=' + FCM_API_KEY,
                        'Content-Type': 'application/json'
                        }
                response = requests.post(FCM_ENDPOINT, json=payload, headers=headers)
                print('Status code:', response.status_code)
                print('Response body:', response.text)



                    #METODA 1 CONTINUARE
                """"  
            
                    # This is the payload for the notification. You can customize it as needed.
                    payload = {
                        "to": DEVICE_TOKEN,
                        "data": {
                            "title": task_model.headline,
                            "body": task_model.deadline,
                        }
                    }

                    # This is the headers for the HTTP request. You should not need to change this.
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"key={SERVER_KEY}",
                    }

                    # This sends the HTTP request to the FCM API.
                    response = requests.post(FCM_URL, json=payload, headers=headers)

                    # This prints the response from the FCM API. You can use this for debugging
                    # or for checking the status of the request.
                    print("raspunsul e")
                    print(response.text)
                    """

            except:
                return HttpResponseRedirect("addTask")
    return HttpResponseRedirect(reverse("addTask"))



def subscribers(request):
  
    subscribers = Subscribe.objects.values('email', 'date_submitted')
    data = {
        'subscribers' : list(subscribers)
    }
    return JsonResponse(data)
 
#@login_required()
def viewAllEmployees(request): 
    user_now = request.user
    active_tasks = Tasks.objects.filter(is_active = 1)
    #tasks = Employee.objects.all()
    employees = User.objects.filter(is_employee=1)
    print(employees)
    print(active_tasks)
    return render(request, 'view_all_employees.html',{'employees': employees,"active_tasks":active_tasks,  })



#@login_required()
def viewAllTasks(request):
    users = User.objects.filter(is_employee=1)
    tasks = Tasks.objects.all()
    if request.method == 'POST':
        form = TaskFilterForm(request.POST)
        if form.is_valid():
            column = form.cleaned_data['column']
            value = form.cleaned_data['value']
            print(column)
            print(value)
            tasks = Tasks.objects.filter(**{column: value})
    else:
        form = TaskFilterForm()
    #fac task urile in functie de ordinea data 
    return render(request, 'view_all_tasks.html',{"tasks":tasks,"users":users,'form': form})

#@login_required()
def viewClosedTasks(request):
    users =User.objects.all()
    tasks = Tasks.objects.all().order_by('-closed_at')
    if request.method == 'POST':
        form = ClosedTaskFilterForm(request.POST)
        if form.is_valid():
            column = form.cleaned_data['column']
            value = form.cleaned_data['value']
            print(column)
            print(value)
            tasks = Tasks.objects.filter(**{column: value})
    else:
        form = TaskFilterForm()
    return render(request, 'view_closed_tasks.html',{"tasks":tasks,"users": users,"form":form})

 
def particularEmployee(request, id):
    employee =User.objects.get(id = id)
    print(employee.id)
    reports = Report.objects.filter(user_id = employee.id).order_by('-current_date')
    tasks = Tasks.objects.filter(user_id = employee.id).order_by('-closed_at')
    return render(request, 'view_particular_employee.html',{ "tasks":tasks,"employee": employee, "reports":reports})




def viewActivity(request, username):
    user_employee =User.objects.get(username = username)
    employee = Employee.objects.get(user_id = user_employee.id)
    tasks = Tasks.objects.filter(user_id = user_employee.id)
    #return render(request, 'view_activity.html',{"employee": employee,"tasks":tasks,"user_employee": user_employee,"january":january})
    return render(request, 'view_activity.html',{"employee": employee,"tasks":tasks,"user_employee": user_employee})



#rapoarte zilnice  
def dailyReport(request, pk):

    user_now = request.user
    employees = User.objects.filter(is_employee=1)
    my_tasks = Tasks.objects.filter(user_id = pk)
    #current_date
    current_date = timezone.now()   
    print(pk)
    rep = Report.objects.get(user_id = pk, current_date__date = current_date.date())
    print("a gasit report?")
    print(rep)
    if not rep:
        report = Report( 
                        user_id = User.objects.get(id = pk), 
                        completed_tasks = 0,
                        uncompleted_tasks = 0,
                        current_date = current_date, 
                        type = "Daily"
                        )
    else:
        report = Report.objects.get(user_id = pk, current_date__date = current_date.date())
    #verificam task uri
    for i in my_tasks:
        #daca au fost inchise azi
        if i.closed_at.date() == current_date.date() and i.is_completed == 1:
            report.completed_tasks +=1
            report.tasks.add(i)
            #print(report.pause_time)
        #daca au ramas active azi
        if i.is_active == 1 and  i.started_at.date() <= current_date.date()  :
            report.uncompleted_tasks +=1
            report.tasks.add(i)

    #aflu cand am inceput si scad de acolo ora 8 ca sa vad cate minute am in prima parte
    first_task = Tasks.objects.filter(user_id = pk, started_at__date = current_date.date() ).order_by('started_at')[:1].first()
    #first_pause = first_task.started_at - datetime.datetime(current_date.year, current_date.month, current_date.day, 8, 0,0)
    last_task = Tasks.objects.filter(user_id = pk, closed_at__date = current_date.date() ).order_by('-closed_at')[:1].first()
    print(last_task)
    count_active = 0
    for task in my_tasks:
        #daca am task activ si inca e in lucru
        if task.is_active == 1 and task.started_at.date() == current_date.date() :
            count_active =1
        #daca am un task inactiv dar a fost pus in una din zilele anterioare
        elif task.is_active == 0 and task.closed_at.date() == current_date.date() and task.started_at.date()<current_date.date():
            count_active =2
        #daca am un task 
        elif task.is_active ==1 and task.task_time ==  task.closed_at.time():
            count_active = 3
    print("COUNT ACTIVE")
    print(count_active)

    #daca gasesc un task activ nu mai fac last_pauze, dar daca nu gasesc il fac
    if count_active ==0:
        attendance = Attendance.objects.filter(user_id = pk, start_time__date = timezone.now().date()).last()
        print(attendance)
        first_pause_start_pause_date = datetime(attendance.start_time.date().year, attendance.start_time.date().month, attendance.start_time.date().day, attendance.start_time.time().hour,attendance.start_time.time().minute,attendance.start_time.time().second)
        first_pause_finish_pause_date = first_task.started_at
        last_pause_start_date = last_task.closed_at 
        last_pause_finish_pause_date = datetime(attendance.end_time.date().year, attendance.end_time.date().month, attendance.end_time.date().day, attendance.end_time.time().hour, attendance.end_time.time().minute,attendance.end_time.time().second)
        today_pause = datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)

        today_pause = today_pause + (first_pause_finish_pause_date-first_pause_start_pause_date)+(last_pause_finish_pause_date - last_pause_start_date)

        print("today pause final")
        print(today_pause)
    #daca un task de azi e inca activ lucrez si maine la el
    elif count_active == 1:
        for i in my_tasks:
            #daca am terminat totusi un task azi
            if i.is_active == 0 and i.closed_at.date() == timezone.now().date():
                attendance = Attendance.objects.filter(user_id = pk, start_time__date = timezone.now().date()).last()
                today_pause = datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
                break
            #altfel
            else:
                attendance = Attendance.objects.filter(user_id = pk, start_time__date = timezone.now().date()).last()
                print(attendance)
                first_pause_start_pause_date = datetime(attendance.start_time.date().year, attendance.start_time.date().month, attendance.start_time.date().day, attendance.start_time.time().hour,attendance.start_time.time().minute,attendance.start_time.time().second)
                first_pause_finish_pause_date = first_task.started_at
                today_pause = datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
                
                today_pause += (first_pause_finish_pause_date-first_pause_start_pause_date)
                
    #daca am un task din alta zi si l-am terminat azi iar acum e inactiv 
    elif count_active == 2:
        attendance = Attendance.objects.filter(user_id = pk, start_time__date = timezone.now().date()).last()
        print(attendance)
        last_pause_start_date = last_task.closed_at 
        last_pause_finish_pause_date = datetime(attendance.end_time.date().year, attendance.end_time.date().month, current_date.day, attendance.end_time.time().hour, attendance.end_time.time().minute,attendance.end_time.time().second)
        today_pause = datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
        
        today_pause += last_pause_finish_pause_date - last_pause_start_date
    elif count_active == 3:
        attendance = Attendance.objects.filter(user_id = pk, start_time__date = timezone.now().date()).last()

    print("TODAY _ PAUSE")
    print(today_pause)
    print("REPORT PAUSE TIME")
    print(report.pause_time)
    print(timedelta(seconds = timedelta(hours = today_pause.hour, minutes = today_pause.minute,seconds = today_pause.second).total_seconds()))
    s =  timedelta(seconds = report.pause_time.total_seconds()*1000000) + timedelta(seconds = timedelta(hours = today_pause.hour, minutes = today_pause.minute,seconds = today_pause.second).total_seconds())
    print("S este")
    print(s)

    report.pause_time = timedelta(seconds = s.total_seconds()/1000000)
    attendance_schedule = (attendance.end_time - attendance.start_time).total_seconds()
    today_work = timedelta(seconds = attendance_schedule)

    report.work_time = timedelta(seconds = (today_work - s).total_seconds()/1000000)
    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Here is your daily report!' ,
    'You have completed '+str(report.completed_tasks)+' tasks. Tasks uncompleted today: '+str(report.uncompleted_tasks),
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)
    #calculez timpul zilnic de lucru 
        
    return render(request, 'view_all_employees.html',{'employees': employees,"user_now ":user_now })




#rapoarte saptamanale 
def weeklyReport(request, pk):
    #ce e din viewallemployees
    user_now = request.user
    employees = User.objects.filter(is_employee=1)

    current_date = timezone.now()
    my_tasks = Tasks.objects.filter(user_id = pk)
    today = timezone.now()

    monday = today - timedelta(days=today.weekday())
    print("MONDAY")
    print(monday)
    try:
        rep = Report.objects.get(current_date__date = timezone.now().date(), r_type = "Weekly")
    except Report.DoesNotExist:
        rep = None
    if not rep:
        report = Report( 
                        user_id = User.objects.get(id = pk), 
                        current_date = current_date, 
                        pause_time = 0,
                        work_time = 0,
                        r_type = "Weekly"
                        )
        report.pause_time = timedelta (seconds = report.pause_time)
        report.work_time = timedelta (seconds = report.work_time)
        print (type(report.work_time))
        
    else:
        report = Report.objects.get(user_id = pk, current_date__date = current_date.date(), r_type = "Weekly")
    report.save()
    for i in my_tasks:
        #extrag doar data
        i_closedat_date = i.closed_at.date()
        #tot started at dar inainte assigned_at era = started_at deci las asa
        i_startedat_date = i.started_at.date()
        i_deadline_date = i.deadline.date()
        
        if i.is_active == 0  and i_closedat_date<=today.date() and i_closedat_date>=monday.date():
            report.tasks.add(i)
        #daca au ramas active dupa saptamana asta
        if i.is_active == 1  and i_startedat_date<=today.date() and i_startedat_date>=monday.date() :
            report.uncompleted_tasks +=1
            report.tasks.add(i)

    reports = Report.objects.filter(user_id = pk, r_type = "Daily")
    for r in reports:
        if r.current_date.date()>=monday.date() and r.current_date<=today:
            report.work_time +=r.work_time
            report.completed_tasks += r.completed_tasks
            
            print (r)
            report.pause_time +=r.pause_time

    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Here is your weekly report!' ,
    'You have completed '+str(report.completed_tasks)+' tasks. Tasks uncompleted today: '+str(report.uncompleted_tasks),
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)
    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':my_tasks,"user_now ":user_now })


#rapoarte lunare 
def monthlyReport(request, pk):
    #ce e din viewallemployees
    user_now = request.user
    employees = User.objects.filter(is_employee=1)
    current_date = timezone.now()
    #toate task urile acelui angajat
    my_tasks = Tasks.objects.filter(user_id = pk)
    #azi e vineri deci o sa fie data sub forma 2023-01-13 de exemplu
    today = timezone.now()
    last_day = calendar.monthrange(today.year, today.month)
    last_day_date = datetime(today.year, today.month, today.date().day)
    first_day_date = datetime(today.year, today.month, 1)
    completed_tasks = 0
    uncompleted_tasks = 0
    try:
        rep = Report.objects.get(current_date__date = timezone.now().date(), r_type = "Monthly")
    except Report.DoesNotExist:
        rep = None
    if not rep:
        report = Report( 
                        user_id = User.objects.get(id = pk), 
                        current_date = current_date, 
                        pause_time = 0,
                        work_time = 0,
                        r_type = "Monthly"
                        )
        report.pause_time = timedelta (seconds = report.pause_time)
        report.work_time = timedelta (seconds = report.work_time)
        print (type(report.work_time))
        
    else:
        report = Report.objects.get(user_id = pk, current_date__date = current_date.date(), r_type = "Weekly")
    report.save()
    for i in my_tasks:
        i_closedat_date = i.closed_at
        i_startedat_date = i.started_at
        i_deadline_date = i.deadline
        #daca au fost inchise luna asta
        if i.is_active == 0 and i_closedat_date<=last_day_date and i_closedat_date>=first_day_date:
            report.tasks.add(i)
        #daca au ramas active dupa luna asta
        if i.is_active == 1 and i_startedat_date<=last_day_date and i_startedat_date>=first_day_date:
            uncompleted_tasks +=1
            report.tasks.add(i)

    reports = Report.objects.filter(user_id = pk, r_type = "Daily")
    for r in reports:
        if r.current_date>=first_day_date and r.current_date<=today:
            report.work_time +=r.work_time
            report.completed_tasks += r.completed_tasks
            
            print (r)
            report.pause_time +=r.pause_time

    report.save()

    
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Here is your monthly report!' ,
    'You have completed '+str(report.completed_tasks)+' tasks. Tasks uncompleted today: '+str(report.uncompleted_tasks),
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)

    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':my_tasks,"user_now ":user_now })


#rapoarte anuale 
def annualReport(request, pk):
     #ce e din viewallemployees
    user_now = request.user
    employees = User.objects.filter(is_employee=1)
    current_date = timezone.now()
    #toate task urile acelui angajat
    my_tasks = Tasks.objects.filter(user_id = pk)
    #azi e vineri deci o sa fie data sub forma 2023-01-13 de exemplu
    today = timezone.now()
    last_day = calendar.monthrange(today.year, today.month)
    last_day_date = datetime(today.year, today.month, today.date().day)
    first_day_date = datetime(today.year, 1, 1)
    completed_tasks = 0
    uncompleted_tasks = 0
    try:
        rep = Report.objects.get(current_date__date = timezone.now().date(), r_type = "Monthly")
    except Report.DoesNotExist:
        rep = None
    if not rep:
        report = Report( 
                        user_id = User.objects.get(id = pk), 
                        current_date = current_date, 
                        pause_time = 0,
                        work_time = 0,
                        r_type = "Monthly"
                        )
        report.pause_time = timedelta (seconds = report.pause_time)
        report.work_time = timedelta (seconds = report.work_time)
        print (type(report.work_time))
        
    else:
        report = Report.objects.get(user_id = pk, current_date__date = current_date.date(), r_type = "Weekly")
    report.save()
    for i in my_tasks:
        i_closedat_date = i.closed_at
        i_startedat_date = i.started_at
        i_deadline_date = i.deadline
        #daca au fost inchise luna asta
        if i.is_active == 0 and i_closedat_date<=last_day_date and i_closedat_date>=first_day_date:
            report.tasks.add(i)
        #daca au ramas active dupa luna asta
        if i.is_active == 1 and i_startedat_date<=last_day_date and i_startedat_date>=first_day_date:
            uncompleted_tasks +=1
            report.tasks.add(i)

    reports = Report.objects.filter(user_id = pk, r_type = "Daily")
    for r in reports:
        if r.current_date>=first_day_date and r.current_date<=today:
            report.work_time +=r.work_time
            report.completed_tasks += r.completed_tasks
            
            print (r)
            report.pause_time +=r.pause_time

    report.save()

    
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Here is your monthly report!' ,
    'You have completed '+str(report.completed_tasks)+' tasks. Tasks uncompleted today: '+str(report.uncompleted_tasks),
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)

    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':my_tasks,"user_now ":user_now })


def viewReport(request, pk):
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

    

"""
def addHoliday(request):
    employees =  User.objects.filter(is_employee=1)
    print(employees)
    return render(request, 'add_holiday.html',{"employees":employees})
"""

def deleteUser(request, pk):   
    try:
        u = User.objects.get(id = pk)
        u.delete()
        #messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        #messages.error(request, "User doesnot exist")    
        return render(request, 'view_all_employees.html')

    except Exception as e: 
        return render(request, 'view_all_employees.html',{'err':e.message})

    return render(request, 'view_all_employees.html') 


def setAttendance(request):
    employees =  User.objects.filter(is_employee=1)
    return render(request, 'attendance.html',{"employees" : employees}) 


def setAttendanceSave(request):
    l = []
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        l = request.POST.getlist("usernames")
        print(l)
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
        a_type = request.POST.get("a_type")
        notes = request.POST.get("notes")
        print(start_time)
        print(end_time)
        print(a_type)
        print(notes)
        if datetime.strptime(end_time, '%Y-%m-%dT%H:%M') - datetime.strptime(start_time, '%Y-%m-%dT%H:%M') == timedelta(seconds = 8*3600) and a_type == "Workday":
            print("SUCCESS")
            #assigned_at =request.POST.get("assigned_at")
            for i in l:
                user = User.objects.get(username = i)
                print(type(user))
                #employee=Employee.objects.get(user_id=user.id)  
                #employee.save()
                try:
                    attendance=Attendance(start_time=start_time, end_time = end_time, a_type = a_type, notes = notes , user_id =user)
                    attendance.save()
                    messages.success(request, "Schedule set successfully!")
                    #METODA 1
                    device = FCMDevice.objects.get(user_id = user.id, active=1)
                    print(device)
                    DEVICE_TOKEN = device.registration_id
                    print("device token e")
                    print(DEVICE_TOKEN)
                    #d = dateutil.parser.parse(task_model.deadline)
                    d1 = dateutil.parser.parse(attendance.start_time)
                    d2 = dateutil.parser.parse(attendance.end_time)
                      
                        #METODA 2
                    FCM_ENDPOINT = 'https://fcm.googleapis.com/fcm/send'
                    FCM_API_KEY = ''
                    payload = {
                            "to": DEVICE_TOKEN,
                            "notification": {
                                "title": "The work schedule has been set!",
                                "body": "Welcome back! This is your schedule: {} - {}  ".format(d1.strftime("%H:%M"),d2.strftime("%H:%M"))  
                            },
                            "android": {
                                "priority": "high"
                            }
                            }
                    headers = {
                            'Authorization': 'key=' + FCM_API_KEY,
                            'Content-Type': 'application/json'
                            }
                    response = requests.post(FCM_ENDPOINT, json=payload, headers=headers)
                    print('Status code:', response.status_code)
                    print('Response body:', response.text)

                    
                except:
                    return redirect("setAttendance")
        elif a_type == "Sick Leave":
            print("SUCCESS")
            #assigned_at =request.POST.get("assigned_at")
            for i in l:
                user = User.objects.get(username = i)
                print(type(user))
                #employee=Employee.objects.get(user_id=user.id)  
                #employee.save()
                try:
                    attendance=Attendance(start_time=start_time, end_time = end_time, a_type = a_type, notes = notes , user_id =user)
                    attendance.save()
                    messages.success(request, "Schedule set successfully!")
                    #METODA 1
                    device = FCMDevice.objects.get(user_id = user.id, active=1)
                    print(device)
                    DEVICE_TOKEN = device.registration_id
                    print("device token e")
                    print(DEVICE_TOKEN)
                    #d = dateutil.parser.parse(task_model.deadline)
                    d1 = dateutil.parser.parse(attendance.start_time)
                    d2 = dateutil.parser.parse(attendance.end_time)
                      

                    FCM_ENDPOINT = 'https://fcm.googleapis.com/fcm/send'
                    FCM_API_KEY = ''
                    payload = {
                            "to": DEVICE_TOKEN,
                            "notification": {
                                "title": "Below is your sick leave period",
                                "body": "{} - {}  ".format(d1.strftime("%Y-%m-%d"),d2.strftime("%Y-%m-%d"))  
                            },
                            "android": {
                                "priority": "high"
                            }
                            }
                    print(payload)
                    headers = {
                            'Authorization': 'key=' + FCM_API_KEY,
                            'Content-Type': 'application/json'
                            }
                    response = requests.post(FCM_ENDPOINT, json=payload, headers=headers)
                    print('Status code:', response.status_code)
                    print('Response body:', response.text)

                    
                    date_list = []
                    d = datetime.strptime(attendance.end_time, '%Y-%m-%dT%H:%M').date() - datetime.strptime(attendance.start_time, '%Y-%m-%dT%H:%M').date()
                    print(date_list)
                    start = datetime.strptime(attendance.start_time, '%Y-%m-%dT%H:%M')
                    while start <= datetime.strptime(attendance.end_time, '%Y-%m-%dT%H:%M'):
                        date_list.append(start)
                        start += timedelta(days=1)
                    print(date_list)
                    i = date_list[0]
                    last = date_list[len(date_list)-1]
                    while i<=last:
                        print(i)
                        report = Report( 
                        user_id = User.objects.get(id = request.user.id), 
                        current_date = i, 
                        completed_tasks = 0, 
                        uncompleted_tasks = 0,
                        r_type = "Daily",
                        work_time = timedelta(seconds = 0 ),
                        pause_time = timedelta(seconds = 0 )
                        )
                        
                        report.save()
                        print(report)
                        i += timedelta(days=1)

                    
                except:
                    return redirect("setAttendance")
        elif a_type == "Holiday":
            print("SUCCESS")
            #assigned_at =request.POST.get("assigned_at")
            for i in l:
                user = User.objects.get(username = i)
                print(type(user))
                #employee=Employee.objects.get(user_id=user.id)  
                #employee.save()
                try:
                    attendance=Attendance(start_time=start_time, end_time = end_time, a_type = a_type, notes = notes , user_id =user)
                    attendance.save()
                    messages.success(request, "Schedule set successfully!")
                    #METODA 1
                    device = FCMDevice.objects.get(user_id = user.id, active=1)
                    print(device)
                    DEVICE_TOKEN = device.registration_id
                    print("device token e")
                    print(DEVICE_TOKEN)
                    #d = dateutil.parser.parse(task_model.deadline)
                    d1 = dateutil.parser.parse(attendance.start_time)
                    d2 = dateutil.parser.parse(attendance.end_time)
                      

                    FCM_ENDPOINT = 'https://fcm.googleapis.com/fcm/send'
                    FCM_API_KEY = ''
                    payload = {
                            "to": DEVICE_TOKEN,
                            "notification": {
                                "title": "Below is your vacation period",
                                "body": "{} - {}  ".format(d1.strftime("%Y-%m-%d"),d2.strftime("%Y-%m-%d"))  
                            },
                            "android": {
                                "priority": "high"
                            }
                            }
                    print(payload)
                    headers = {
                            'Authorization': 'key=' + FCM_API_KEY,
                            'Content-Type': 'application/json'
                            }
                    response = requests.post(FCM_ENDPOINT, json=payload, headers=headers)
                    print('Status code:', response.status_code)
                    print('Response body:', response.text)

                    
                    date_list = []
                    d = datetime.strptime(attendance.end_time, '%Y-%m-%dT%H:%M').date() - datetime.strptime(attendance.start_time, '%Y-%m-%dT%H:%M').date()
                    print(date_list)
                    start = datetime.strptime(attendance.start_time, '%Y-%m-%dT%H:%M')
                    while start <= datetime.strptime(attendance.end_time, '%Y-%m-%dT%H:%M'):
                        date_list.append(start)
                        start += timedelta(days=1)
                    print(date_list)
                    i = date_list[0]
                    last = date_list[len(date_list)-1]
                    while i<=last:
                        print(i)
                        report = Report( 
                        user_id = User.objects.get(id = request.user.id), 
                        current_date = i, 
                        completed_tasks = 0, 
                        uncompleted_tasks = 0,
                        r_type = "Daily",
                        work_time = timedelta(seconds = 0 ),
                        pause_time = timedelta(seconds = 0 )
                        )
                        
                        report.save()
                        print(report)
                        i += timedelta(days=1)

                    
                except:
                    return redirect("setAttendance")
        else:
            messages.error(request, "The schedule does not respect the rules!")
    return redirect("setAttendance")
    #return render(request, "attendance.html")
