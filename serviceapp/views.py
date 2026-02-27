from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customuser,Department,Services,Users,review,tasks,Profile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import hashers,login,logout,authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import random
import string
import os
# Create your views here.

# # pages


# home
def home(request):
    spdata=Users.objects.filter(user__user_type='1', user__status=1).select_related('user','department','service').order_by('department__name')   

    return render(request,'home.html',{'spdata':spdata}) 

@login_required(login_url='signin')
def worker(request):
    user= Users.objects.get(user=request.user)

    reviews=review.objects.filter(task__service_provider=user)
    cus=Customuser.objects.get(id=user.user.id)

    total_reviews = reviews.count()
    stats = []
    for i in range(5, 0, -1):
        if total_reviews > 0:
            count = reviews.filter(rating=i).count()
            percent = (count / total_reviews) * 100
        else:
            percent = 0
        stats.append({'rating': i, 'percent': percent})
   
    data=Profile.objects.filter(user=cus)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()


    return render(request,'worker.html',{'user':user,'data':data,'reviews':reviews,'stats':stats,'reqcount':reqcount})
@login_required(login_url='signin')
def customer(request):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0)
    spdata=Users.objects.filter(user__user_type='1', user__status=1).select_related('user','department','service').order_by('department__name')   
    query=request.GET.get('q')
    if query:
        spdata=spdata.filter(Q (department__name__icontains=query) | Q(service__name__icontains=query))
        return render(request,'customer.html',{'depdata':depdata,'spdata':spdata,'user':user,'query':query})
    else:
        return render(request,'customer.html',{'depdata':depdata,'spdata':spdata,'user':user})
@login_required(login_url='signin')
def admin(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    noti=users+dtotal
    print('noti',noti)

    data=Department.objects.filter(status=0)
    sdata=Services.objects.filter(status=0)

    
 
    return render(request,'admin.html',{'utotal':users,'dtotal':dtotal,'total':total,'data':data,'sdata':sdata,'noti':noti})



def signin(request):
    return render(request,'signin.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

# registration pages
def regworker(request):
    
    dep=Department.objects.filter(status=0)
    return render(request,'regworker.html',{'dep':dep})

def regcustomer(request):
    return render(request,'regcustomer.html')

@login_required(login_url='signin')
def regdepartment(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    return render(request,'regdepartment.html',{'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def regservice(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data=Department.objects.all()
    return render(request,'regservice.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def viewsp(request):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    data=Users.objects.filter(user__user_type='1')
    return render(request,'viewproviders.html',{'spdata':data,'depdata':depdata,'user':user})


@login_required(login_url='signin')
def viewspdetails(request,id):
    pdata=Users.objects.get(id=id)
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    cus=Customuser.objects.get(id=pdata.user.id)
    reviews=review.objects.filter(task__service_provider=pdata)
    data=Profile.objects.filter(user=cus)
    total_reviews = reviews.count()
    stats = []
    for i in range(5, 0, -1):
        if total_reviews > 0:
            count = reviews.filter(rating=i).count()
            percent = (count / total_reviews) * 100
        else:
            percent = 0
        stats.append({'rating': i, 'percent': percent})
   
    return render(request,'viewspdetails.html',{'pdata':pdata,'data':data,'reviews':reviews,'stats':stats,'depdata':depdata,'user':user})

@login_required(login_url='signin')
def viewcustask(request):
    udata=Users.objects.get(user=request.user)
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    data=tasks.objects.filter(user=udata).prefetch_related('review_set')
    # reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'viewcustask.html',{'data':data,'depdata':depdata,'user':user})


@login_required(login_url='signin')
def viewcurtask(request):
    udata=Users.objects.get(user=request.user.id)
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    print('udata',udata)
    data=tasks.objects.filter(service_provider=udata,a_status=1)
    print('data',data)
    # data=tasks.objects.filter(user=udata)
    print('data',data)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'viewcurtask.html',{'data':data,'depdata':depdata,'user':user,'reqcount':reqcount})


@login_required(login_url='signin')
def viewtaskrequest(request):
    udata=Users.objects.get(user=request.user)
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    print(udata)
    data=tasks.objects.filter(service_provider=udata)
    print(data)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'viewtaskrequest.html',{'data':data,'depdata':depdata,'user':user,'reqcount':reqcount})

@login_required(login_url='signin')
def history(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal    
    ur=Users.objects.get(id=id)
    
    uid = get_object_or_404(Customuser, id=ur.user.id)

    user = get_object_or_404(Users, user=uid)

    # Prefetch reviews to avoid N+1 queries in the template
    data=tasks.objects.filter(service_provider=user).prefetch_related('review_set')
    
    return render(request,'history.html',{'data':data,'total':total,'dtotal':dtotal,'users':users,'depuser':depuser})


@login_required(login_url='signin')
def profile(request):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    uid=request.user.id
    uid=Users.objects.get(user=uid)
    data=Users.objects.get(user=request.user)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'viewprofile.html',{'data':data,'uid':uid,'user':user,'depdata':depdata,'reqcount':reqcount})


@login_required(login_url='signin')
def profilecus(request):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    uid=request.user.id
    uid=Users.objects.get(user=uid)
    data=Users.objects.get(user=request.user)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'profilecus.html',{'data':data,'uid':uid,'user':user,'depdata':depdata,'reqcount':reqcount})

@login_required(login_url='signin')
def profileworker(request):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    uid=request.user.id
    uid=Users.objects.get(user=uid)
    data=Users.objects.get(user=request.user)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'profileworker.html',{'data':data,'uid':uid,'user':user,'depdata':depdata,'reqcount':reqcount})

@login_required(login_url='signin')
def viewserindep(request,id):
    user=Users.objects.get(user=request.user)
    depdata=Department.objects.filter(status=0) 
    data=Users.objects.filter(department__id=id, user__user_type='1', user__status=1).select_related('user','department','service')
    ddata=Department.objects.get(id=id)
    return render(request,'viewserindep.html',{'data':data,'dedata':ddata,'user':user,'depdata':depdata})

@login_required(login_url='signin')
def viewapproveldata(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    noti=users+dtotal
    data=Users.objects.get(id=id)
    return render(request,'viewapproveldata.html',{'data':data,'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser})

@login_required(login_url='signin')
def view_content(request):
    user=Users.objects.get(user=request.user)
    reviews=review.objects.filter(task__service_provider=user)
    cus=Customuser.objects.get(id=user.user.id)
    depdata=Department.objects.filter(status=0)

    total_reviews = reviews.count()
    stats = []
    for i in range(5, 0, -1):
        if total_reviews > 0:
            count = reviews.filter(rating=i).count()
            percent = (count / total_reviews) * 100
        else:
            percent = 0
        stats.append({'rating': i, 'percent': percent})
   
    data=Profile.objects.filter(user=cus)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'view_content.html',{'data':data,'user':user,'reviews':reviews,'stats':stats,'depdata':depdata,'reqcount':reqcount})

@login_required(login_url='signin')
def view_rating(request):
    user=Users.objects.get(user=request.user)
    data=review.objects.filter(task__service_provider=user)
    return render(request,'view_rating.html',{'data':data})

@login_required(login_url='signin')
def depapprovels(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    dedata=Department.objects.filter(status=1)
    sedata=Services.objects.filter(status=1)
    return render(request,'adepapprovels.html',{'dedata':dedata,'sedata':sedata,'utotal':users,'dtotal':dtotal,'total':total})


# authentication

# viewapprovels
@login_required(login_url='signin')
def viewapprovels(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data=Users.objects.all().exclude(user__user_type='2')
    return render(request,'viewapprovels.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def approveserv(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    data=Services.objects.get(id=id)
    return render(request,'approveserv.html',{'data':data,'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser})

@login_required(login_url='signin')
def approvedep(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    ddata=Department.objects.get(id=id)
    return render(request,'approveserv.html',{'ddata':ddata,'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser})

@login_required(login_url='signin')
def apdept(request,id):
    data=Services.objects.get(id=id)
    depdata=Department.objects.get(id=data.department.id)
    
    name=request.POST['dept_name']
    dep=Department.objects.filter(name=name).exclude(id=data.department.id)
    if dep:
        messages.info(request,'Department alredy exist')
        return redirect('approveserv', id=id)
    else:
        depdata.name=name
        depdata.description=request.POST['dept_description']
        depdata.image=request.FILES.get('dept_image') 
        depdata.status=0
        depdata.save()
        messages.info(request,'department approved')    
        return redirect('approveserv', id=id)

def aprovdept(request,id):
    depdata=Department.objects.get(id=id)
    name=request.POST['dept_name']
    dep=Department.objects.filter(name=name).exclude(id=id)
    if dep:
        messages.info(request,'Department alredy exist')
        return redirect('depapprovels')
    else:
        depdata.name=request.POST['dept_name']
        depdata.description=request.POST['dept_description']
        depdata.image=request.FILES.get('dept_image') 
        depdata.status=0
        depdata.save()
        messages.info(request,'department approved')    
        return redirect('depapprovels')


def apserv(request,id):
    data=Services.objects.get(id=id)
    data.name=request.POST['serv_name']
    data.description=request.POST['serv_description']
    data.status=0
    data.save()
    messages.info(request,'service approved')    
    return redirect('approveserv', id=id)


def rejserv(request,id):
    data=Services.objects.get(id=id)
    user=get_object_or_404(Users,service=data)
    cust=Customuser.objects.get(id=user.user.id)
    email=user.user.email
    send_mail('Rejection mail',
              f""" sorry to inform this we have desided to reject your requset for being a service provider with username  {user.user.username} """,
              settings.EMAIL_HOST_USER,
              [email]
              )
    
    user.delete()
    cust.delete()
    data.delete()
    messages.info(request,'user and service rejected')
    return redirect('viewapprovels')


def rejdept(request,id):
    data=Services.objects.get(id=id)
    depdata=Department.objects.get(id=data.department.id)
    user=get_object_or_404(Users,service=data)
    cust=Customuser.objects.get(id=user.user.id)
    email=user.user.email
    send_mail('Rejection mail',
              f""" sorry to inform this we have desided to reject your requset for being a service provider with username  {user.user.username} """,
              settings.EMAIL_HOST_USER,
              [email]
              )
    user.delete()
    cust.delete()
    depdata.delete()
    messages.info(request,'user and department rejected')
    return redirect('viewapprovels')

def rejectdepart(request,id):
    
    depdata=Department.objects.get(id=id)
    user=user=get_object_or_404(Users,department=depdata)
    cust=Customuser.objects.get(id=user.user.id)
    cust.delete()

    
    depdata.delete()
    messages.info(request,'user and department rejected')
    return redirect('depapprovels')


def approveworker(request,id):
    data=Customuser.objects.get(id=id)
    data.status=1
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special=random.choice(string.punctuation)
    others = "".join(random.choices(string.ascii_letters + string.digits, k=4))
    pass1 = "".join(random.sample(upper + special + digit + others, 7))
    data.set_password(pass1)
    email=data.email
    uname=data.username

    data.save()
    send_mail('Confidential Email',
                  f""" This email contais confidential contents please do not share it with any one.

                  Admin has approved you request for being a service provider.

                  Now you have successfuly registered as {uname} .
                  Use this password to login {pass1}

                  Dont share your password with anyone
                  Thank you for becoming a service provider with us
                 """,
                  settings.EMAIL_HOST_USER,
                  [email]
                  
                  )
    messages.info(request,'user approved')
    return redirect('viewapprovels')



def rejectworker(request,id):
    data=Customuser.objects.get(id=id)
    email=data.email
    send_mail('Rejection mail',
               f""" sorry to inform this we have desided to reject your requset for being a service provider with username  {data.username} """,
              settings.EMAIL_HOST_USER,
              [email]
              )
    data.delete()
    messages.info(request,'user rejected')
    return redirect('viewapprovels')




def accepttask(request,id):
    data=tasks.objects.get(id=id)
    data.a_status=1
    data.save()
    messages.info(request,'task accepted')
    return redirect('viewtaskrequest')


def rejecttask(request,id):
    data=tasks.objects.get(id=id)
    data.a_status=2
    data.save()
    messages.info(request,'task rejected')
    return redirect('viewtaskrequest')
# view pages

@login_required(login_url='signin')
def viewworker(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data=Users.objects.filter(user__user_type='1', user__status=1)
    return render(request,'viewworker.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def viewcustomer(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data = Users.objects.filter(user__user_type='2')    
    return render(request,'viewcustomer.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def viewdept(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data=Department.objects.filter(status=0)
    
    print(data)
    return render (request,'viewdept.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def viewserv(request):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    
    data=Services.objects.filter(status=0)
    
    print(data)
    return render (request,'viewserv.html',{'data':data,'total':total,'dtotal':dtotal,'utotal':users,'depuser':depuser})

@login_required(login_url='signin')
def regtaskpage(request,id):
    data=Users.objects.get(id=id)
    sdata=Services.objects.filter(department=data.department)
    uid=request.user.id
    user=Customuser.objects.get(id=uid)
    
    udata=Users.objects.get(user=user)


    
    return render(request,'regtask.html',{'data':data,'sdata':sdata,'udata':udata})

@login_required(login_url='signin')
def profile_content(request):
    uid=request.user
    user=Users.objects.get(user=uid)
    data=Users.objects.get(user=request.user)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()

    return render(request,'profile_content.html',{'data':data,'user':user,'reqcount':reqcount})

# edit

@login_required(login_url='signin')
def edit_worker(request):
    data=Users.objects.get(user=request.user)

    reqcount=tasks.objects.filter(service_provider=data,a_status=0).count()

    return render(request,'editprow.html',{'data':data,'user':data,'reqcount':reqcount})

@login_required(login_url='signin')
def edituser(request):
    data=Users.objects.get(user=request.user)
    return render(request,'edituser.html',{'data':data,'user':data})
@login_required(login_url='signin')
def edit_dep(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal
    data=Department.objects.get(id=id)
    return render(request,'editdepartment.html',{'data':data,'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser})

@login_required(login_url='signin')
def edit_ser(request,id):
    users=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').count()
    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    dep=Department.objects.filter(status=1).count()
    ser=Services.objects.filter(status=1).count()
    dtotal=dep+ser
    total=users+dtotal 
    data=Services.objects.get(id=id)
    ddata=Department.objects.filter(status=0)
    return render(request,'editservice.html',{'data':data,'ddata':ddata,'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser})

@login_required(login_url='signin')
def changepassword(request):
    userid=request.user
    user=Users.objects.get(user=userid)


    return render(request,'changepassword.html',{'data':user,'user':user})

@login_required(login_url='signin')
def changeworkerpass(request):
    user=Users.objects.get(user=request.user)
    reqcount=tasks.objects.filter(service_provider=user,a_status=0).count()
    return render(request,'changeworkerpass.html',{'user':user,'reqcount':reqcount})

@login_required(login_url='signin')
def changecustonerpass(request):
    user=Users.objects.get(user=request.user)
    return render(request,'changecustomerpass.html',{'user':user})


@login_required(login_url='signin')
def edit_profile_content(request,id):
    user=Users.objects.get(user=request.user)
    data=Profile.objects.get(id=id)
    return render(request,'edit_profile_content.html',{'data':data,'user':user})



# registeration


def r_dept(request):
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        image=request.FILES.get('image')
        dep=Department.objects.filter(name=name)
        if dep:
            messages.info(request,'department already exists')
            return redirect('regdepartment')
        else:

            data=Department(name=name,description=description,image=image)
            data.save()
            messages.info(request,'department sucessfully registered')
            return redirect('viewdept')
    return render(request,'regdepartment.html')

def r_serv(request):
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        dep=request.POST['depatment']
        department=Department.objects.get(id=dep)
        if Services.objects.filter(name=name).exists():
            messages.info(request,'service already exists')
            return redirect('regservice')
        else:
            data=Services(name=name,description=description,department=department)
            data.save()
            messages.info(request,'service sucessfully registered')
            return redirect('viewserv')
    return render(request,'regservice.html')


def r_worker(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        
        phone=request.POST['phone']
        address=request.POST['address']
       
        image = request.FILES.get('image')
        file = request.FILES.get('file')
        id_proof = request.FILES.get('id_proof')
        
        dep = request.POST.get('department')
        cname=Customuser.objects.filter(username=uname)
        if cname:
            messages.info(request,'username already exists')
            return redirect('regworker')
        cemail=Customuser.objects.filter(email=email)
        if cemail:
            messages.info(request,'email already exists')
            return redirect('regworker')
        uphone=Users.objects.filter(phone=phone)
        if uphone:
            messages.info(request,'phone number already exists')
            return redirect('regworker')
        else:
        
            department = None
            service = None
            if dep == 'other':
                # Create new Department and Service
                dep_name = request.POST['dep_name']
                dep_description = request.POST['dep_description']
                depart=Department.objects.filter(name=dep_name)
                if depart:
                    messages.info(request,'department already exists')
                    return redirect('regworker')
                else:
                    department = Department.objects.create(name=dep_name, description=dep_description, status=1)
                    
                    serv_name = request.POST['serv_name']
                    serv_description = request.POST['serv_description']
        
                    service = Services.objects.create(name=serv_name, description=serv_description, department=department, status=1)
            else:
                # Use existing Department and Service
                department = Department.objects.get(id=dep)
                serv_id = request.POST.get('service')
                if serv_id:
                    service = Services.objects.get(id=serv_id)

            user=Customuser(first_name=fname,last_name=lname,username=uname,email=email,user_type='1')
            user.save()
            data=Users(department=department,service=service,user=user,phone=phone,address=address,image=image,file=file,id_proof=id_proof)
            data.save()
            messages.info(request,'worker sucessfully registered please wait for admin approval')
            return redirect('regworker')
        
        # Pass context if GET request (though usually handled by regworker view)
    dep = Department.objects.all()
    return render(request,'regworker.html', {'dep': dep})



def r_customer(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        image=request.FILES.get('image')
        
        # Generate password: min 1 Capital, min 1 digit, length 6
        upper = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special=random.choice(string.punctuation)
        others = "".join(random.choices(string.ascii_letters + string.digits, k=4))
        pass1 = "".join(random.sample(upper + special + digit + others, 7))
        cname=Customuser.objects.filter(username=uname)
        
        if cname:
            messages.info(request,'username already exists')
            return redirect('regcustomer')
        cemail=Customuser.objects.filter(email=email)
        if cemail:
            messages.info(request,'email already exists')
            return redirect('regcustomer')
        uphone=Users.objects.filter(phone=phone)
        if uphone:
            messages.info(request,'phone number already exists')
            return redirect('regcustomer')
        else:

            cdata=Customuser.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1,user_type='2')
            cdata.save()
            data=Users(phone=phone,address=address,user=cdata,image=image)
            data.save()
            cdata.set_password(pass1)
            data.save()
            send_mail('Confidential Email',
                    f""" This email contais confidential contents please do not share it with any one.
                    
                    You have successfuly registered as {uname} .
                    Use this password to login {pass1}

                    Dont share your password with anyone
                    Thank you for registering with us
                    """,
                    settings.EMAIL_HOST_USER,
                    [email]
                    
                    )
            
            messages.info(request,'customer sucessfully registered check your emial for password')
            return redirect('regcustomer')
    return render(request,'regcustomer.html')



    #  edit   # 

def editprofile(request):
    data=Users.objects.get(user=request.user)
    user=Customuser.objects.get(id=data.user.id)
    if request.method=='POST':
        user.first_name=request.POST['fname']
        user.last_name=request.POST['lname']
        
        data.address=request.POST['address']
        uname=request.POST['uname']
        email=request.POST['email']
        phone=request.POST['phone']
        if Customuser.objects.filter(username=uname).exclude(id=data.user.id):
            messages.info(request,'username already exists')
            if user.user_type=='1':
                return redirect('edit_worker')
            else:
                return redirect('edituser')
        if Customuser.objects.filter(email=email).exclude(id=data.user.id):
            messages.info(request,'email already exists')
            if user.user_type=='1':
                return redirect('edit_worker')
            else:
                return redirect('edituser')
        if Users.objects.filter(phone=phone).exclude(user=user):
            messages.info(request,'phone number already exists')
            if user.user_type=='1':
                return redirect('edit_worker')
            else:
                return redirect('edituser')
        
        user.username=request.POST['uname']
        user.email=request.POST['email']
        
        data.phone=request.POST['phone']
        if 'image' in request.FILES:
            img=request.FILES['image']
            if data.image:
                if os.path.exists(data.image.path):
                    os.remove(data.image.path)
            data.image=img


        user.save()
        data.save()
        messages.info(request,'profile updated')
        if user.user_type=='1':
            return redirect('edit_worker')
        else:
            return redirect('edituser')
    # return render(request,'editproprofile.html',{'data':data,'user':user})



def chpassword(request):
    if request.method=='POST':
        old=request.POST['old']
        new=request.POST['new']
        con=request.POST['con']
        user=request.user
        usr=Users.objects.get(user=user)

        if not check_password(old,user.password):
            messages.info(request,'old password not matched')
            if usr.user.user_type=='1':
                return redirect('changeworkerpass')
            else:
                return redirect('changecustonerpass')
        else:
            if old==new:
                    messages.info(request,'old and new password are same please enter different password')
                    if usr.user.user_type=='1':
                        return redirect('changeworkerpass')
                    else:
                        return redirect('changecustonerpass')
            if len(new) < 6 or not any(i.isupper() for i in new) or not any(i in '~`!@#$%^&*)(_+-=][{|}\;:<>/?,."' for i in new) or not any(i.isdigit() for i in new):
                    messages.info(request, 'password must contain uppercase letters, numbers, special characters and minimum 6 characters')
                    if usr.user.user_type=='1':
                        return redirect('changeworkerpass')
                    else:
                        return redirect('changecustonerpass')
            else:
                if new==con:
                    user.set_password(new)
                    user.save()
                    messages.info(request,'password updated')
                    return redirect('signin')
                else:
                    messages.info(request,'password not matched')
                    if usr.user.user_type=='1':
                        return redirect('changeworkerpass')
                    else:
                        return redirect('changecustonerpass')
            

    return render(request,'changepassword.html')


def e_serv(request,id):
    data=Services.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']
        if Services.objects.filter(name=name).exclude(id=id):
            messages.info(request,'service already exists')
            return redirect('edit_ser',id=id)
        data.name=request.POST['name']
        data.description=request.POST['description']
        dep=request.POST['department']
        department=Department.objects.get(id=dep)
        data.department=department
        data.save()
        messages.info(request,'service edited sucessfully')
        return redirect('viewserv')

def e_dep(request,id):
    data=Department.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']
        if Department.objects.filter(name=name).exclude(id=id):
            messages.info(request,'department already exists')
            return redirect('edit_dep',id=id)
        data.name=name
        data.description=request.POST['description']
        if 'image' in request.FILES:
            img = request.FILES['image']
            if data.image:
                try:
                    if os.path.exists(data.image.path):
                        os.remove(data.image.path)
                except Exception:
                    pass
            # always assign the new upload regardless of whether an old file existed
            data.image = img
        data.save()
        messages.info(request,'department edited sucessfully')
        return redirect('viewdept')

def e_profilecon(request,id):
    data=Profile.objects.get(id=id)
    if request.method=='POST':
        head=request.POST['header']
        desc=request.POST['content']
        img=request.FILES.get('image')
        if data.image:
            if os.path.exists(data.image.path):
                os.remove(data.image.path)
        data.image=img
        data.heading=head
        data.description=desc
        data.save()
        messages.info(request,'profile edited sucessfully')
        return redirect('view_content')
    
#  delete

def d_user(request,id):
    data=Users.objects.get(id=id)
    cus=Customuser.objects.get(id=data.user.id)
    email=data.user.email
    send_mail('Rejection mail',
              f"""dear {data.user.first_name} {data.user.last_name} we have desided to delete your account with username  {data.user.username} """,
              settings.EMAIL_HOST_USER,
              [email]
              )
    cus.delete()
    messages.info(request,'user deleted')
    return redirect('viewworker')

def d_serv(request,id):
    data=Services.objects.get(id=id)
    users=Users.objects.filter(service=data)
    if users:
        for i in users:
            cus=Customuser.objects.get(id=i.user.id)
            email=cus.email
            send_mail('Rejection mail',
                f"""dear {cus.first_name} {cus.last_name} sorry to inform this we have desided to delete Service {data.name}. so your account with username  {cus.username} will be deleted. 
                    if u are  interested in any other department please register again""",
                settings.EMAIL_HOST_USER,
                [email]
                )
            cus.delete()
    data.delete()
    messages.info(request,'service deleted')
    return redirect('viewserv')

def d_dep(request,id):
    data=Department.objects.get(id=id)
    users=Users.objects.filter(department=data)
    if users:
        for i in users:
            cus=Customuser.objects.get(id=i.user.id)
            email=cus.email
            send_mail('Rejection mail',
                f"""dear {cus.first_name} {cus.last_name} sorry to inform this we have desided to delete department {data.name}. so your account with username  {cus.username} will be deleted. 
                    if u are  interested in any other department please register again""",
                settings.EMAIL_HOST_USER,
                [email]
                )
            cus.delete()
    
    data.delete()
    messages.info(request,'department deleted')
    return redirect('viewdept')

def d_pro_con(request,id):
    data=Profile.objects.get(id=id)
    data.delete()
    messages.info(request,'profile deleted')
    return redirect('view_content')


# authentication

def log(request):
    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        user=authenticate(username=uname,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('admin')
            elif user.user_type == '1' and user.status == 1:
                login(request,user)
                return redirect('worker')
            elif user.user_type == '2':
                login(request,user)
                return redirect('customer')
            else:
                messages.info(request, 'Your account is pending admin approval.')
                return redirect('signin')
        else:
            messages.info(request,'invalid username or password')
            return redirect('signin')



def out(request):
    logout(request)
    return redirect('home')



def search(request):
    query=request.GET['q']




def regTask(request,id):
    spdata=Users.objects.get(id=id)
    udata=Users.objects.get(user=request.user)

    if request.method=='POST':
        serv=request.POST['services']
        location=request.POST['location']
        date=request.POST['date']
        details=request.POST['details']
        image=request.FILES.get('image')
        service=Services.objects.get(id=serv)   
        data=tasks(service_provider=spdata,user=udata,service=service,location=location,date=date,details=details,image=image)
        data.save()
        messages.info(request, 'task sucessfully registered')
    return redirect('viewcustask')

def complete(request,id):
    data=tasks.objects.get(id=id)
    data.c_status=1
    data.save()
    messages.info(request,'task completed')
    return redirect('viewcurtask')

def pending(request,id):
    data=tasks.objects.get(id=id)
    data.c_status=0
    data.save()
    messages.info(request,'task pending')
    return redirect('viewcurtask')


def add_review(request,id):
    data=tasks.objects.get(id=id)
    pid=data.service_provider.id
    if request.method=='POST':
        revie=request.POST['review']
        rating=int(request.POST['starvalue'])
        dat=review(task=data,review=revie,rating=rating)
        dat.save()
        messages.info(request,'review added')
        return redirect('viewcustask')
    return redirect('viewcustask')

def reg_profile(request):
    uid=request.user.id
    user=Customuser.objects.get(id=uid)
    if request.method=='POST':
        head=request.POST['header']
        desc=request.POST['content']
        image=request.FILES.get('image')
        data=Profile(user=user,heading=head,description=desc,image=image)
        data.save()
        return redirect('profile_content')



# ajax

def getserv(request):
    id=request.GET['id']
    data=Department.objects.get(id=id)
    serv=Services.objects.filter(department=data)
    data=[{'id':i.id,'name':i.name,'description':i.description} for i in serv]
    return JsonResponse({'data':data,})



#

# validations
def checkuname(request):
    uname=request.GET['username']
    user=Customuser.objects.filter(username=uname).exists()
    return JsonResponse({'user':user})


def chackmail(request):
    email=request.GET['email']
    user=Customuser.objects.filter(email=email).exists()
    return JsonResponse({'user':user})


def chackphone(request):
    phone=request.GET['phone']
    user=Users.objects.filter(phone=phone).exists()
    return JsonResponse({'user':user})

def echeckuname(request):
    id=request.user.id
    uname=request.GET['username']
    user=Customuser.objects.filter(username=uname).exclude(id=id).exists()
    return JsonResponse({'user':user})


def echackmail(request):
    id=request.user.id
    
    email=request.GET['email']
    user=Customuser.objects.filter(email=email).exclude(id=id).exists()
    return JsonResponse({'user':user})


def echackphone(request):
    id = request.GET.get('id')
   
    phone = request.GET.get('phone')
    # Check if phone exists excluding the current customer ID
    user = Users.objects.filter(phone=phone).exclude(id=id).exists()
    return JsonResponse({'user':user})

    

def notification(request):
    user=Users.objects.filter(user__user_type='1', user__status=0).select_related('user','department').order_by('-id')
    users=user.count()

    depuser=Users.objects.filter(department__status=1,user__user_type='1',user__status=0).count()
    depa=Department.objects.filter(status=1).order_by('-id')
    dep=depa.count()
    serv=Services.objects.filter(status=1).order_by('-id')
    ser=serv.count()
    dtotal=dep+ser
    total=users+dtotal
    # Build a mixed list of items (type + object + comparable key)
    mixed = []
    for u in user:
        mixed.append({'type': 'user', 'obj': u, 'key': u.id})
    for d in depa:
        mixed.append({'type': 'department', 'obj': d, 'key': d.id})
    for s in serv:
        mixed.append({'type': 'service', 'obj': s, 'key': s.id})

    # Sort mixed list newest first by key (uses id as proxy for recency)
    mixed.sort(key=lambda x: x['key'], reverse=True)
    print(mixed)

    data = {'user': user, 'depa': depa, 'serv': serv, 'mixed': mixed}

    return render(request,'notification.html',{'utotal':users,'dtotal':dtotal,'total':total,'depuser':depuser,'user':user,'depa':depa,'serv':serv,'data':data,'mixed':mixed})
