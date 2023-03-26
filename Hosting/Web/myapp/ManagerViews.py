from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from urllib3 import HTTPResponse
from .forms import ManagerSignUpForm, EmployeeSignUpForm
from .models import  User, Tasks, Report
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
import datetime
from datetime import timedelta
import numpy as np
import calendar
from django.core.mail import send_mail
from.filters import TaskFilterForm,ClosedTaskFilterForm


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
        #assigned_at =request.POST.get("assigned_at")
        for i in l:
            user = User.objects.get(username = i)
            #employee=Employee.objects.get(user_id=user.id)  
            #employee.save()
            try:
                task_model=Tasks(headline=headline, body = body, deadline = deadline, user_id = user,task_type = task_type)
                task_model.author = request.user
                print(task_type)
                task_model.save()
                print("task saved")
                print("user id")
                print(user.id)
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
    return render(request, 'view_all_employees.html',{'employees': employees,"active_tasks":active_tasks })

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

 
def particularEmployee (request, username):
    employee =User.objects.get(username = username)
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
    #ce e din viewallemployees
    user_now = request.user
    employees = User.objects.filter(is_employee=1)
    my_tasks = Tasks.objects.filter(user_id = pk)
    #current_date
    current_date = timezone.now()   
    completed_tasks = 0
    uncompleted_tasks = 0
    for i in my_tasks:
        #daca au fost inchise azi
        if i.closed_at.date() == current_date.date() and i.is_completed == 1:
            completed_tasks +=1
            
        #daca au ramas active azi
        if i.is_active == 1 and  i.started_at.date() <= current_date.date()  :
            uncompleted_tasks +=1

    #task uri realizate azi =  task-uri terminate la timp sau dupa timp = completed_tasks
    rep = Report.objects.get(user_id = request.user.id, current_date__date = current_date.date())
    print("a gasit report?")
    print(rep)
    if not rep:
        report = Report( 
                        user_id = User.objects.get(id = pk), 
                        current_date = current_date, 
                        completed_tasks = completed_tasks, 
                        uncompleted_tasks = uncompleted_tasks,
                        type = "Daily"
                        )
    else:
        report = Report.objects.get(user_id = request.user.id, current_date__date = current_date.date())
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
    print(count_active)

    #daca gasesc un task activ nu mai fac last_pauze, dar daca nu gasesc il fac
    if count_active ==0:
        first_pause_start_pause_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 8, 0,0)
        first_pause_finish_pause_date = first_task.started_at
        last_pause_start_date = last_task.closed_at 
        last_pause_finish_pause_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 16, 0,0)
        today_pause = datetime.datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
        
        today_pause += (first_pause_finish_pause_date-first_pause_start_pause_date)
        today_pause += (last_pause_finish_pause_date - last_pause_start_date)
    #daca un task de azi e inca activ lucrez si maine la el
    elif count_active == 1:
        first_pause_start_pause_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 8, 0,0)
        first_pause_finish_pause_date = first_task.started_at
        #first_pause.save()
        today_pause = datetime.datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
        
        today_pause += (first_pause_finish_pause_date-first_pause_start_pause_date)
                #first_pause.delete()
    #daca am un task din alta zi si l-am terminat azi iar acum e inactiv 
    elif count_active == 2:
        last_pause_start_date = last_task.closed_at 
        last_pause_finish_pause_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 16, 0,0)
        today_pause = datetime.datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
        
        today_pause += last_pause_finish_pause_date - last_pause_start_date
    elif count_active == 3:
        today_pause =today_pause = datetime.datetime(current_date.year, current_date.month, current_date.day, 0, 0,0)
    print("today_pause")
    print(today_pause)

    #minutes
    today_work = datetime.datetime(current_date.year, current_date.month, current_date.day, 8, 0,0)
    report.pause_hours = today_pause.time().hour
    report.pause_minutes = today_pause.time().minute
    seconds_working_hours = (today_work - datetime.datetime(current_date.year, current_date.month, current_date.day, report.pause_hours, report.pause_minutes,0)).seconds
    report.working_hours = seconds_working_hours//3600
    working_minutes = (seconds_working_hours/3600 - int(seconds_working_hours/3600)) *60
    report.working_minutes = working_minutes

    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('You have completed {report.completed_tasks} tasks. Tasks uncompleted today: {report.uncompleted_tasks} ',
    'Message',
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
    #toate task urile acelui angajat
    my_tasks = Tasks.objects.filter(user_id = pk)
    #azi e vineri deci o sa fie data sub forma 2023-01-13 de exemplu
    today = datetime.date.today()
    #asa aflu data zilei de luni sub forma 2023-01-09 de exemplu
    monday = today - datetime.timedelta(days=today.weekday())
    #am initializat iar cu 0 variabilele astea
    completed_tasks = 0
    uncompleted_tasks = 0
    for i in my_tasks:
        #extrag doar data
        i_closedat_date = i.closed_at.date()
        #tot started at dar inainte assigned_at era = started_at deci las asa
        i_startedat_date = i.started_at.date()
        i_deadline_date = i.deadline.date()
        #daca au fost inchise saptamana asta 
        if i.is_active == 0  and i_closedat_date<=today and i_closedat_date>=monday:
            completed_tasks +=1
        #daca au ramas active dupa saptamana asta
        if i.is_active == 1  and i_startedat_date<=today and i_startedat_date>=monday :
            uncompleted_tasks +=1
        
        
    report = Report(
                    user_id = User.objects.get(id = pk), 
                    current_date = current_date, 
                    completed_tasks = completed_tasks, 
                    uncompleted_tasks = uncompleted_tasks,
                    type = "Weekly"
                    )
    


    reports = Report.objects.filter(user_id = pk)
    w_hours = 0
    w_minutes = 0
    p_hours = 0
    p_minutes = 0
    for i in reports:
        if i.current_date.date() <=today and i.current_date.date() >=monday and i.type == 0:
            print(i)
            w_hours += i.working_hours
            w_minutes += i.working_minutes
            p_hours += i.pause_hours
            p_minutes += i.pause_minutes
    if w_minutes >= 60:
        w_hours += int(w_minutes/60)
    if p_minutes >= 60:
        p_hours += int(p_minutes/60)
    print(w_hours)
    #ex 124 - 2*60 = 4 min 
    w_minutes = w_minutes - int(w_minutes/60)*60 
    p_minutes = p_minutes - int(p_minutes/60)*60
    report.working_hours = w_hours
    report.working_minutes = w_minutes
    report.pause_hours = p_hours
    report.pause_minutes = p_minutes
    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Your daily report is ready to check!',
    'Message',
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)
    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':tasks,"user_now ":user_now })


#rapoarte lunare 
def monthlyReport(request, pk):
    #ce e din viewallemployees
    user_now = request.user
    tasks = Employee.objects.all()
    employees = User.objects.filter(is_employee=1)
    

    current_date = timezone.now()
    #toate task urile acelui angajat
    my_tasks = Tasks.objects.filter(user_id = pk)
    #azi e vineri deci o sa fie data sub forma 2023-01-13 de exemplu
    today = datetime.date.today()
    #(31, 1)  asa arata 
    last_day = calendar.monthrange(today.year, today.month)
    #2023-01-31 de exemplu
    last_day_date = datetime.date(today.year, today.month, last_day[0])
    first_day_date = datetime.date(today.year, today.month, 1)
    completed_tasks = 0
    uncompleted_tasks = 0
    for i in my_tasks:
        i_closedat_date = i.closed_at.date()
        i_startedat_date = i.started_at.date()
        i_deadline_date = i.deadline.date()
        #daca au fost inchise luna asta
        if i.is_active == 0 and i_closedat_date<=last_day_date and i_closedat_date>=first_day_date:
            completed_tasks +=1
        #daca au ramas active dupa luna asta
        if i.is_active == 1 and i_startedat_date<=last_day_date and i_startedat_date>=first_day_date:
            uncompleted_tasks +=1


        report = Report(
                    user_id = User.objects.get(id = pk), 
                    current_date = current_date, 
                    completed_tasks = completed_tasks, 
                    uncompleted_tasks = uncompleted_tasks,
                    type = "Monthly"
                    )
    

    reports = Report.objects.filter(user_id = pk)
    w_hours = 0
    w_minutes = 0
    p_hours = 0
    p_minutes = 0
    for report in reports:
        if report.current_date.date() <=last_day_date and report.current_date.date() >=first_day_date and report.type == "Weekly":
            w_hours += report.working_hours
            w_minutes += report.working_minutes
            p_hours += report.pause_hours
            p_minutes += report.pause_minutes
    if w_minutes >= 60:
        w_hours += int(w_minutes/60)
    if p_minutes >= 60:
        p_hours += int(p_minutes/60)
    #ex 124 - 2*60 = 4 min 
    w_minutes = w_minutes - int(w_minutes/60)*60 
    p_minutes = p_minutes - int(p_minutes/60)*60
    report.working_hours = w_hours
    report.working_minutes = w_minutes
    report.pause_hours = p_hours
    report.pause_minutes = p_minutes
    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Your daily report is ready to check!',
    'Message',
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)

    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':tasks,"user_now ":user_now })


#rapoarte anuale 
def annualReport(request, pk):
    #ce e din viewallemployees
    user_now = request.user
    tasks = Employee.objects.all()
    employees = User.objects.filter(is_employee=1)



    current_date = timezone.now()
    #toate task urile acelui angajat
    my_tasks = Tasks.objects.filter(user_id = pk)
    #azi e vineri deci o sa fie data sub forma 2023-01-13 de exemplu
    today = datetime.date.today()
    #2023-01-31 de exemplu
    last_day_date = datetime.date(today.year, 12, 30)
    first_day_date = datetime.date(today.year, 1, 1)
    #am initializat iar cu 0 variabilele astea
    completed_tasks = 0
    uncompleted_tasks = 0
    for i in my_tasks:
        i_closedat_date = i.closed_at.date()
        i_startedat_date = i.started_at.date()
        i_deadline_date = i.deadline.date()
        #daca au fost inchise anul asta
        if i.is_active == 1 and i_closedat_date<=last_day_date and i_closedat_date>=first_day_date:
            completed_tasks +=1
        #daca au ramas active dupa anul asta
        if i.is_active == 0 and i_startedat_date >= first_day_date and i_startedat_date <= last_day_date:
            uncompleted_tasks +=1


    report = Report(
                    user_id = User.objects.get(id = pk), 
                    current_date = current_date, 
                    completed_tasks = completed_tasks, 
                    uncompleted_tasks = uncompleted_tasks,
                    type = "Annual"
                    )
    

    reports = Report.objects.filter(user_id = pk)
    w_hours = 0
    w_minutes = 0
    p_hours = 0
    p_minutes = 0
    for report in reports:
        if report.current_date.date() <=last_day_date and report.current_date.date() >=first_day_date and report.type == 2:
            w_hours += report.working_hours
            w_minutes += report.working_minutes
            p_hours += report.pause_hours
            p_minutes += report.pause_minutes
    if w_minutes >= 60:
        w_hours += int(w_minutes/60)
    if p_minutes >= 60:
        p_hours += int(p_minutes/60)
    #ex 124 - 2*60 = 4 min 
    w_minutes = w_minutes - int(w_minutes/60)*60 
    p_minutes = p_minutes - int(p_minutes/60)*60
    report.working_hours = w_hours
    report.working_minutes = w_minutes
    report.pause_hours = p_hours
    report.pause_minutes = p_minutes
    
    report.save()
    user_email = User.objects.get(id = report.user_id.id)
    send_mail('Your daily report is ready to check!',
    'Message',
    'jurubitamiruna@gmail.com',
    [user_email.email],
    fail_silently=False,
)
    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':tasks,"user_now ":user_now })


def viewReport(request, pk):
    report = Report.objects.get(id = pk)
    r_date = report.current_date.date()
    print(report.id)
    #daily
    #tasks1 daca sunt inchide cand a fost raportul
    #tasks2 daca s a inceput taskul cand s a facut raportul
    #tasks3 daca a avut deadline atunci is e activ
    #tasks4 daca am avut deadline atunci si e complet
    tasks1 = Tasks.objects.filter(user_id = report.user_id, closed_at__date = report.current_date.date(), is_completed = 1)
    tasks2 = Tasks.objects.filter(user_id = report.user_id, started_at__date = report.current_date.date(), is_active = 1)
    #tasks3 = Tasks.objects.filter(user_id = report.user_id, deadline__date = report.current_date.date(),is_completed = 0, is_active = 0)
    #tasks4 = Tasks.objects.filter(user_id = report.user_id, deadline__date = report.current_date.date(),is_completed = 1)

    #weekly
    #monthly
    #annual
    return render(request, 'view_report.html',{"report":report,"tasks1":tasks1,"tasks2":tasks2})

    

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