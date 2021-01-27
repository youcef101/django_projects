from django.shortcuts import render,redirect
from django.http import HttpResponse
def notLoggedUser(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


# def allowedUser(allowed_role=[]):
#     def decorator(view_func):
#         def wrapper_func(request,*args,**kwargs):
#             group=None
#             if request.user.groups.exists():
#                 group=request.user.groups.all()[0].name
#             if group in allowed_role:
#                 return view_func(request,*args,**kwargs)
#             else:
#                 return HttpResponse('you are not authorized to view this page')
#         return wrapper_func
#     return decorator 



def forAdmin(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists:
            group = request.user.groups.all()[0].name
        if group=='admin':
            return view_func(request, *args, **kwargs)
        if group=='customer':
            return redirect('product')
            
    return wrapper_func
