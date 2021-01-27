from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group,User
from .models import*
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
import requests
from django.conf import settings


# Create your views here.
@login_required(login_url='login')
#@allowedUser(allowed_role=['admin'])
@forAdmin
def home(request):
    context={}
    return render(request,'accounts/dashboard.html',context)


@notLoggedUser
def userRegister(request):
    if request.method=='POST':
        form=createNewUser(request.POST)
        if form.is_valid():
            #***********************Recaptcha****************************
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
            #************************************
                # "commit=False " This is useful if you want to do custom processing on the object before saving it,
                # or if you want to use one of the specialized model saving options.
                # commit is True by default.
              user = form.save(commit=False)
            #***************************
              user.is_active = False
              user.save()
            #---------------------------------------------------------------
              username = form.cleaned_data.get('username')
              email = form.cleaned_data.get('email')
              instance = User.objects.get(username=username)
              group = Group.objects.get(name='customer')
              users = user.groups.add(group)
              Customer.objects.create(user=instance, Name=username, Email=email)
            #--------------------------------------------------------------------
              current_site = get_current_site(request)
              message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
              })
              mail_subject = 'Activate your blog account.'
              to_email = form.cleaned_data.get('email')
              email = EmailMessage(mail_subject, message, to=[to_email])
              email.send()
              return HttpResponse('Please confirm your email address to complete the registration')
            #**************************************************
              messages.success(request, username + ' successfully created')
              return redirect('login')
              #*******************Recaptcha**************
        else:
            messages.error(request,  ' invalid Recaptcha please try again!')
            #*******************************************

    else:
        form = createNewUser()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

#********************************Email Activation Function*******************************
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
       
        return render(request,'accounts/email_confirmation_done.html')
    else:
        return HttpResponse('Activation link is invalid!')
#*********************************************************


@notLoggedUser
def userLogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # if user.is_staff:
            return redirect('home')
            # if not user.is_staff:
            #   return redirect('product')
        else:
            messages.info(request,'credentials error')
    context = {}
    return render(request, 'accounts/login.html', context)


def userLogout(request):
   logout(request)
   return redirect('login')


@login_required(login_url='login')
def userInfo(request):
    context = {}
    return render(request, 'accounts/last_order.html', context)


@login_required(login_url='login')
def userSettings(request):
    customer=request.user.customer
    form=customerForm(instance=customer)
    if request.method=='POST':
        form = customerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
#@allowedUser(allowed_role=['customer'])
def product(request):
    context = {}
    return render(request, 'accounts/products.html', context)
