from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        #or user.username == 'admin'
        if user.is_authenticated:
            if user.is_admin == 1:
                if modulename == "myapp.ManagerViews":
                    pass
                elif modulename == "myapp.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("managerPage"))
                    """
            elif user.is_employee == 1:
                if modulename == "myapp.EmployeeViews":
                    pass
                elif modulename == "myapp.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("employeePage"))

            else:
                return HttpResponseRedirect(reverse("loginUser"))

        else:
            if request.path == reverse("loginUser"):
                pass
            #else:
            #    return HttpResponseRedirect(reverse("loginUser"))
        """
