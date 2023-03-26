from myapp.models import User, Tasks, Report, Pause , Attendance
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from django.utils import timezone
import datetime 
import numpy as np
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
import requests
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from datetime import datetime, timedelta, time

@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    try:
        data = request.data
        try:
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user.is_employee and user.is_active:
                registration_token = data.get('token')
                fcm_device = FCMDevice()
                fcm_device.registration_id = registration_token
                fcm_device.user_id = user.id
                devices = FCMDevice.objects.all()
                ok = 1
                for dev in devices:
                    if dev.registration_id == fcm_device.registration_id and dev.user_id == fcm_device.user_id:
                        ok = 0
                if ok == 1:
                    fcm_device.save()
                login(request,user)
                serializer = serializers.SignInSerializer(user)
                return Response({"result": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"parameter error": "User type is not an employee OR not Active!"},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"parameter error": "Incorrect username/Password!"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"Exception Occur: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def dashboard(request):
    if request.method == 'GET':
        try:
            auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
            user = Token.objects.get(key=auth_token).user
            tasks = Tasks.objects.filter(user_id=user.id, is_completed = 0).order_by('deadline')
            paginator = PageNumberPagination()
            paginator.page_size = 1000
            mlist = [{'id': task.id, "is_active":task.is_active,'headline': task.headline,
            'body':task.body,'assigned_at':task.assigned_at, 'deadline':task.deadline} for task in tasks]
            #print(mlist)
            result_page = paginator.paginate_queryset(mlist, request)
            serializer = serializers.TaskSerializer(result_page, many=True)
            #print(serializer.data)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
                return Response({"parameter error": str(e) + "OR Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def start(request, task_id):
    if request.method == 'PUT':
        try:
            auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
        except Exception as e:
            return Response({"parameter error": str(e) + "OR Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

        task = Tasks.objects.get(pk=task_id)
        task.started_at = timezone.now()
        task.is_active = 1
        #employee = Employee.objects.get(id = task.employee_id.id)
        #employee.active_tasks = employee.active_tasks +1
        #employee.is_busy = 1
        #employee.save()
        task.save()
        #pun stop la pauza
        #imi aleg toate task urile mele
        my_tasks = Tasks.objects.filter(user_id = task.user_id)
        count = 0
        for i in my_tasks:
            if i.is_active == 1 and i.id !=task_id:
                count +=1
        print(count)
        print(task.user_id)
        try:
            rep = Report.objects.get(current_date__date = timezone.now().date())
        except Report.DoesNotExist:
            rep = None
        
        #daca nu am rapoarte si nu am task uri active    
        if not rep and count == 0:
            report = Report( 
                            user_id = task.user_id, 
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

        if task:
            return Response({"result": "Task Started"}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({"parameter error": "Task not Updated"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def startPause(request, task_id):
    if request.method == 'PUT':
        try:
            auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
        except Exception as e:
            return Response({"parameter error": str(e) + "OR Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        task = Tasks.objects.get(pk=task_id)
        pause = Pause.objects.create(task_id = Tasks.objects.get(id = task_id), start_pause_date = timezone.now())
        pause.save()
        if task:
            return Response({"result": "Pause Started"}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({"parameter error": "Pause not Updated"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def stopPause(request, task_id):
    if request.method == 'PUT':
        try:
            auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
        except Exception as e:
            return Response({"parameter error": str(e) + "OR Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        task = Tasks.objects.get(pk=task_id)
        pause = Pause.objects.filter(task_id = task_id).order_by('-start_pause_date').first()
        print(pause)
        pause.finish_pause_date = timezone.now()
        pause.pause_time += timedelta(seconds= (pause.finish_pause_date- pause.start_pause_date).total_seconds()/1000000)
        try:
            rep = Report.objects.get(current_date__date = timezone.now().date())
        except Report.DoesNotExist:
            rep = None
        
        #daca nu am rapoarte si nu am task uri active    
        if not rep:
            report = Report( 
                            user_id = task.user_id, 
                            current_date = timezone.now(), 
                            completed_tasks = 0, 
                            uncompleted_tasks = 0,
                            r_type = "Daily",
                            work_time = timedelta(seconds = 0 ),
                            pause_time = timedelta(seconds = 0 )
                            )
            report.save()
        else:
            report = Report.objects.get(current_date__date = timezone.now().date())
            print(timezone.now().time())
            report.pause_time +=pause.pause_time

            report.current_date = timezone.now()
            report.save()

        report = Report.objects.get(user_id = task.user_id,current_date__date = timezone.now().date())
        s = report.pause_time.total_seconds()+pause.pause_time.total_seconds()
        print("total seconds pause time")
        print(pause.pause_time.total_seconds())
        print("treport.pause_time")
        print(report.pause_time.total_seconds())

        report.pause_time = timedelta(seconds = s)
        print(report.pause_time)
        print(type(s))
        print(pause.finish_pause_date)
        task.pause_time += pause.pause_time
        pause.save()
        report.save()
        task.save()
        if task:
            return Response({"result": "Pause Finished"}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({"parameter error": "Pause not Updated"}, status=status.HTTP_404_NOT_FOUND)





@api_view(['PUT'])
def completed(request, task_id):
    if request.method == 'PUT':
        try:
            auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
        except Exception as e:
            return Response({"parameter error": str(e) + "OR Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

        task = Tasks.objects.filter(pk=task_id).update(is_active = False)
        task_timecalc = Tasks.objects.get(id= task_id)
        if task_timecalc.is_active == 1:
            task_timecalc.is_active = 0   
            task_timecalc.is_completed = 1 
        if task_timecalc:
            task_timecalc.closed_at = timezone.now()
            if task_timecalc.closed_at > task_timecalc.deadline:
                task_timecalc.is_overdue=1
                
  
            diff = abs(task_timecalc.started_at - task_timecalc.closed_at)

            if task_timecalc.closed_at.date() == task_timecalc.started_at.date():
                time_of_work = int(diff.total_seconds()/60)*60
                task_timecalc.task_time = timedelta(seconds=time_of_work)/1000000
                print(task_timecalc.task_time)
            else:
                if task_timecalc.closed_at.day - task_timecalc.assigned_at.day == 1:
                    attendance1 = Attendance.objects.get(start_time__date = task_timecalc.started_at.date())
                    attendance2 = Attendance.objects.get(start_time__date = timezone.now().date())
                    time_of_work = diff.total_seconds() - (attendance2.start_time-attendance1.end_time).total_seconds()

                    task_timecalc.task_time = timedelta(seconds=time_of_work)/1000000 
                elif task_timecalc.closed_at.day - task_timecalc.started_at.day > 1 or task_timecalc.closed_at.month!=task_timecalc.started_at.month:
                    l = []
                    attendances = Attendance.objects.filter(user_id = task_timecalc.user_id)
                    for i in range(0, len(attendances)-1):
                        if attendances[i].start_time <= timezone.now():
                                time_of_work = diff.total_seconds() - (attendances[i+1].start_time-attendances[i].end_time).total_seconds()
                    closed_at_date = task_timecalc.closed_at.date()
                    assigned_at_date = task_timecalc.started_at.date()
                    weekend_days = np.busday_count(assigned_at_date, closed_at_date, weekmask='0000011')
                    time_of_work = time_of_work - 24*weekend_days*3600

                    task_timecalc.task_time = timedelta(seconds=time_of_work)/1000000
            
            #task_timecalc.task_effective_time = str(datetime.combine(datetime.today(), datetime.strptime(task_timecalc.task_time, "%H:%M:%S").time())  - datetime.combine(datetime.today(), task_timecalc.pause_time))
            task_timecalc.task_effective_time = timedelta(seconds = (task_timecalc.task_time.total_seconds())) - task_timecalc.pause_time
            print("task_time")
            print(task_timecalc.task_time)
            
            print(task_timecalc.pause_time)
            task_timecalc.is_completed = 1
            task_timecalc.save()
            #print(time_of_work)

            

            my_tasks = Tasks.objects.filter(user_id = task_timecalc.user_id, is_active = 1)
            count1 = 0
            #numar sa vad daca am task uri active la momentul cand inchid taskul 
            for i in my_tasks:
                #if i.is_active == 1 and i.id !=id:
                if i.id !=id:
                    count1 +=1
            reports = Report.objects.filter(user_id = task_timecalc.user_id)
            count2 =  0
            for i in reports:
                if i.current_date.date() == timezone.now().date():
                    count2 +=1
            if count1 == 0 and count2 == 0:
                report = Report( 
                            user_id = User.objects.get(id = task_timecalc.user_id).id, 
                            current_date = timezone.now(), 
                            completed_tasks = 0, 
                            uncompleted_tasks = 0,
                            type = "Daily"
                            )
                report.save()
            return Response({"result": "Mark as Completed"}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({"parameter error": "Task not Updated"}, status=status.HTTP_404_NOT_FOUND)


       


@api_view(['POST'])
def mark_all_uncompleted(request):
    auth_token = str(request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[1]
    user = Token.objects.get(key=auth_token).user

    tasks = Tasks.objects.filter(is_active=True).update(is_active=False)
    data = {
        "id": 1,
        "is_active": 1,
        "is_overdue": 0,
        "headline": "Testing Task 2.5",
        "body": "2 Task body description",
        "assigned_at": "2022-08-20T18:24:53.398049",
        "closed_at": "2022-08-25T18:22:36.438763",
        "deadline": "2022-09-14T18:29:00",
        "hours": 0,
        "minutes": 0,
        "days": 0,
        "seconds": 0,
        "is_active": True,
        "employee_id": 2,
        "user_id": 3
    }
    ser = serializers.TaskSerializers(data=data)

    if ser.is_valid():
        ser.save()
        print(ser.data)
    else:
        print("ser.errors")
        print(ser.errors)

    # users = User.objects.all()
    # for user in users:
    #     print(user.id)
    #     print(Employee.objects.filter(user=user)[0].id)
    #     print(user.username)
    #     print("__________________________________")

    if tasks:
        return Response({"result": "Mark as uncompleted"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"parameter error": "Task not Updated"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def savetask(request):
    if request.method == "POST":
        task = serializers.TaskSerializerAdd(data=request.data)
        task.save()
        print("200")
        return Response(task.data)


def collectdata(request):
    if request.method == "POST":
        headline=request.POST.get("headline")
        body=request.POST.get("body")
        deadline = request.POST.get("deadline")
        employee_id=request.POST.get("employee")
        user = User.objects.get(id = employee.user_id)
        employee=Employee.objects.get(user_id=employee_id)  
        employee.active_tasks = employee.active_tasks +1
        employee.save()
        headers= {'Content-Type: "application/json"'}
        data = {"headline":headline,"body":body,"deadline":deadline,"employee_id":employee_id,"user_id":user}
        apipath = requests.post('http://192.168.1.6:8000/employee-api/savetask', data=data, headers=headers)
        return HttpResponseRedirect(reverse("addTask"))
    else:
        return HttpResponseRedirect("addTask")



