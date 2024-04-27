from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings



# class Courses(models.Model):
#     CourseName = models.CharField(max_length=500)

#     def __str__(self):
#         return self.CourseName

# class Years(models.Model):
#     Name = models.CharField(max_length=500)

#     def __str__(self):
#         return self.Name



class MyUserManager(BaseUserManager):
    def create_user(self, email,username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your username is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    



class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone",default="+255", max_length=13)

    # Course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True,null=True)
    # Year = models.ForeignKey(Years, on_delete=models.CASCADE, blank=True,null=True)
    
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True






class Classes(models.Model):
    
    ClassName = models.CharField(verbose_name="Class Name" ,max_length=200, blank=True, null=True)
    ClassFee = models.IntegerField(verbose_name="Total Fee", default=0, blank=True, null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.ClassName


    class Meta:
        verbose_name_plural = "Classes"




class Students(models.Model):
    
    Class = models.ForeignKey(Classes, on_delete=models.CASCADE, blank=True,null=True)
    StudentName = models.CharField(verbose_name="Student Full Name" ,max_length=200, blank=True, null=True)
    #TotalFee = models.IntegerField(verbose_name="Total Fee", default='0', blank=True, null=True)
    
    ReceivedBy = models.CharField(verbose_name="ReceivedBy", max_length=200, blank=True, null=True)
    IssuedBy = models.CharField(verbose_name="IssuedBy", max_length=200, blank=True, null=True)
    
    ParentNumber = models.CharField(verbose_name="Parent Phone Number",max_length=14, blank=True, null=True)
    StudentLocation = models.CharField(verbose_name="Student Location",max_length=200, blank=True, null=True)

    student_gender = (
            (' ', 'Chooces Gender'),
            ('Male', 'Male'),
            ('Female', 'Female')

        )
    Gender = models.CharField(max_length=50, verbose_name="Student Gender",choices=student_gender, blank=True, null=True)
    


    ReceivedAmount = models.IntegerField(verbose_name="Received Amount", default=0, blank=True, null=True)
    StatusFee = models.IntegerField(verbose_name="Paid Amount",default=0, blank=True, null=True)
    AmountRemained = models.IntegerField(verbose_name="Amount Remained",default=0, blank=True, null=True)
    AmountExceed = models.IntegerField(verbose_name="Amount Exceed",default=0, blank=True, null=True)
    IssuedAmount = models.IntegerField(verbose_name="Issued Amount", default=0, blank=True, null=True)
    

    last_updated = models.DateTimeField(auto_now_add=False,auto_now=True, blank=True, null=True )
    
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    
    StudentImage = models.ImageField(verbose_name="Student Image", upload_to='media/StudentImages', blank=True, null=True)
    is_finished =models.BooleanField(default=False, blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True, blank=True, null=True)
        
    
    #is_received = models.BooleanField(default=False)

    #def lifespan(self):
        #return '%s - present' % self.last_updated.strftime('%d/%m/%Y')

    #export_to_CSV = models.BooleanField(default=False)
    def __str__(self):
        return self.StudentName


    class Meta:
        verbose_name_plural = "Students"



