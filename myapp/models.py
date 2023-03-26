#from django.contrib.auth.models import AbstractUser
from django.db import models
from tkinter import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta

#from fcm.models import AbstractDevice


# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Admin', default=False)
    is_employee = models.BooleanField('Employee', default=False)

"""
class Managers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()
    #def __str__(self):
    #    return self.user.username 



class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    #number_of_completed_tasks = models.IntegerField(default = 0)
    active_tasks = models.IntegerField(default = 0)
    completed_tasks = models.IntegerField(default = 0)
    is_busy = models.IntegerField(default = 0)
    #def __str__(self):
    #   return self.user.username   
"""

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    #employee_id = models.ForeignKey(Employee,blank=True,null=True,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    is_active = models.IntegerField(default = 0)
    is_completed = models.IntegerField(default = 0)
    is_overdue = models.IntegerField(default = 0)
    headline = models.CharField(max_length = 100)
    body = models.TextField()
    dflt = timezone.now()
    assigned_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(default = dflt)
    closed_at =  models.DateTimeField(default = dflt)
    deadline = models.DateTimeField(default = dflt)
    default = timezone.now().time()
    task_time = models.DurationField(default=timedelta())
    pause_time = models.DurationField(default=timedelta())
    task_type = models.CharField(max_length = 25, default = 'Normal')
    task_effective_time = models.DurationField(default=timedelta())


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    #employee_id = models.ForeignKey(Employee,blank=True,null=True,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    dflt = timezone.now()
    r_type = models.CharField(max_length = 15, default = "Daily")
    current_date =  models.DateTimeField(default = dflt)
    completed_tasks = models.IntegerField(default = 0)
    uncompleted_tasks = models.IntegerField(default = 0)
    work_time = models.DurationField(default = "00:00:00")
    pause_time = models.DurationField(default = "00:00:00")
    tasks = models.ManyToManyField(Tasks)
    
    """
    working_hours = models.IntegerField(default = 0)
    working_minutes = models.IntegerField(default = 0)
    pause_hours = models.IntegerField(default = 0)
    pause_minutes = models.IntegerField(default = 0)
    """

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    start_time = models.DateTimeField()
    end_time =models.DateTimeField()
    a_type = models.CharField(max_length = 40)
    notes = models.CharField(max_length = 500)

class Pause(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    dflt = timezone.now()
    start_pause_date =  models.DateTimeField(default = dflt)
    finish_pause_date =  models.DateTimeField(default = dflt)
    pause_time = models.DurationField(default=timedelta())
    location =  models.TextField(default ="")
    pause_details = models.TextField(default ="")


