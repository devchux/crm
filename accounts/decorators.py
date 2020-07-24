from django.shortcuts import redirect
from django.http import HttpResponse

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request)
            elif group == 'customer':
                return redirect('user')
    return wrapper_func

def admin_customer(view_func):
    def wrapper_func(request, pk, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return view_func(request, pk)
            elif group == 'customer':
                return redirect('user')
    return wrapper_func

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request)
    return wrapper_func

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_roles:
                    return view_func(request)
                else:
                    print(group)
                    return HttpResponse('You are not authorized to view this page')
            
        return wrapper_func
    return decorator