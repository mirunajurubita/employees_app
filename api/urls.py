from . import views
from django.urls import path, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path("signin/", views.signin),
    path("dashboard/", views.dashboard),
    path("completed/<int:task_id>/", views.completed),
    path("start/<int:task_id>/", views.start),
    path("mark-all-tasks-uncomplete/", views.mark_all_uncompleted),
    path('', include(router.urls)),
    path("savetask/", views.savetask, name="savetask"),
    path("collectdata/", views.collectdata, name="collectdata"),
    path("startpause/<int:task_id>/", views.startPause, name="startpause"),
    path("stoppause/<int:task_id>/", views.stopPause, name="stoppause"),
]
