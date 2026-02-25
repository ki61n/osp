from django.db import models
from django.contrib.auth.models import AbstractUser,User
# Create your models here.


class Customuser(AbstractUser):
    user_type=models.CharField(max_length=200,null=True,default=0)
    status=models.IntegerField(default=0)



class Department(models.Model):
    name=models.CharField(max_length=200,null=True)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to='department/',null=True,blank=True)
    status=models.IntegerField(default=0)


class Services(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True)
    description=models.TextField(null=True)
    status=models.IntegerField(default=0)


class Users(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    service=models.ForeignKey(Services,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(Customuser,on_delete=models.CASCADE,null=True)
    phone=models.CharField(max_length=200,null=True)
    address=models.TextField(null=True)
    image=models.ImageField(upload_to='profile',null=True,blank=True)
    file=models.FileField(upload_to='files',null=True,blank=True)
    id_proof=models.FileField(upload_to='id_proof',null=True,blank=True)


class tasks(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE,null=True)
    service_provider=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,related_name='provider_tasks')
    user=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,related_name='user_tasks')
    location=models.CharField(max_length=200,null=True)
    date=models.DateField(null=True)
    details=models.TextField(null=True)
    image=models.ImageField(upload_to='tasks',null=True,blank=True)
    a_status=models.IntegerField(default=0)
    c_status=models.IntegerField(default=0)
    
class review(models.Model):
    task=models.ForeignKey(tasks,on_delete=models.CASCADE,null=True)
    review=models.TextField(null=True)
    rating=models.IntegerField(default=0)

class Profile(models.Model):
    user=models.ForeignKey(Customuser,on_delete=models.CASCADE,null=True)
    heading=models.CharField(max_length=200,null=True)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to='profile',null=True,blank=True)



    
