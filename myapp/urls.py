from django.urls import path, include,re_path
from . import views 
from myapp import ManagerViews, EmployeeViews
#reset password 
from django.contrib.auth import views as auth_views


#from .apiviews import 
urlpatterns = [

    path('', views.index, name = 'index'),
    path('loginUser', views.loginUser, name = 'loginUser'),
    #path('loginPage', views.loginPage, name = 'loginPage'),

    
    path('registerEmployee', ManagerViews.EmployeeSignUpView.as_view(), name='registerEmployee'),
    path('registerAdmin', ManagerViews.ManagerSignUpView.as_view(), name='registerAdmin'),    
    path('logoutUser', views.logoutUser, name = 'logoutUser'),
    path('managerPage', ManagerViews.manager_page, name = 'managerPage'),
    path('employeePage', EmployeeViews.employee_page, name = 'employeePage'),
    path("addTask", ManagerViews.addTask, name = "addTask"),
    path("addTaskSave", ManagerViews.addTaskSave, name = "addTaskSave"),
    path("viewAllEmployees", ManagerViews.viewAllEmployees, name = "viewAllEmployees"),
    path("viewClosedTasks", ManagerViews.viewClosedTasks, name = "viewClosedTasks"),
    path("viewActiveTasks/", EmployeeViews.viewActiveTasks, name = "viewActiveTasks"),
    path("viewAllTasks", ManagerViews.viewAllTasks, name = "viewAllTasks"),
    path('viewActiveTasks/endTask/<int:id>', EmployeeViews.endTask, name='endTask'),
    path('viewActiveTasks/startTask/<int:id>', EmployeeViews.startTask, name='startTask'),
    path('viewActiveTasks/editTask/<int:id>', EmployeeViews.editTask, name='editTask'),
    path('viewActiveTasks/editTask/editTaskSave/<int:id>', EmployeeViews.editTaskSave, name='editTaskSave'),
    path('viewActiveTasks/editTask/editTaskSave/<int:id>', EmployeeViews.editTaskSave, name='editTaskSave'),
    path('onlyEdit/<int:id>', EmployeeViews.onlyEdit, name='onlyEdit'),
    path('onlyEdit/onlyEditSave/<int:id>', EmployeeViews.onlyEditSave, name='onlyEditSave'),
    path("viewActiveTasks/endPause/<int:id>", EmployeeViews.endPause, name = "endPause"),
    path("viewAttendance", EmployeeViews.viewAttendance, name = "viewAttendance"),
    path("editAttendance", EmployeeViews.editAttendance, name = "editAttendance"),

    #path('addTaskSave/<int:deadline>', ManagerViews.addTaskSave, name='addTaskSave'),
    path("employeeClosedTasks", EmployeeViews.employeeClosedTasks, name = "employeeClosedTasks"),
    path("particularEmployee/<int:id>", ManagerViews.particularEmployee, name = "particularEmployee"),
    path("viewActivity/<int:pk>", ManagerViews.viewActivity, name = "viewActivity"),
    #path("report", ManagerViews.report, name = "report"),
    path("dailyReport/<int:pk>", ManagerViews.dailyReport, name = "dailyReport"),
    path("weeklyReport/<int:pk>", ManagerViews.weeklyReport, name = "weeklyReport"),
    path("monthlyReport/<int:pk>", ManagerViews.monthlyReport, name = "monthlyReport"),
    path("annualReport/<int:pk>", ManagerViews.annualReport, name = "annualReport"),
    path("setAttendance", ManagerViews.setAttendance, name = "setAttendance"),
    path("setAttendanceSave", ManagerViews.setAttendanceSave, name = "setAttendanceSave"),
    path("particularEmployee/viewReport/<int:pk>", ManagerViews.viewReport, name = "viewReport"),
    path("viewMyReports", EmployeeViews.viewMyReports, name = "viewMyReports"),
    #path("addHoliday", ManagerViews.addHoliday, name = "addHoliday"),
    path("viewReport/<int:pk>", EmployeeViews.viewReport, name = "viewReport"),
    #path("startPause", EmployeeViews.startPause, name = "startPause"),
    
    #path("resetPassword", views.resetPassword, name = "resetPassword"),
    #path("addEmployee", ManagerViews.addEmployee, name = "addEmployee"),
    path("deleteUser/<int:pk>", ManagerViews.deleteUser, name = "deleteUser"),

    path('adminPage', views.adminPage, name = 'adminPage'),
   
   #reset password 
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset/reset_password.html'), name="reset_password"),
    path('reset-link-sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset/reset_password_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset/reset_password_form.html'), name="password_reset_confirm"),
    path('reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset/reset_password_done.html'), name="password_reset_complete"),

]

