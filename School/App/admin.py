from django.contrib import admin
from .models import *
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class MyUserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_active')
    search_fields=('email','username', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'first_name', 'middle_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

class StudentsAdmin(admin.ModelAdmin):
    list_display = ['StudentName','Class','StatusFee', 'StudentLocation', 'Gender', 'ParentNumber', 'created','last_updated']
    list_filter=['created','last_updated']
    search_fields = ["StudentName"]



class ClassesAdmin(admin.ModelAdmin):
    list_display = ['ClassName','ClassFee','Created','Updated']
    list_filter=['Created','Updated']
    search_fields = ["ClassName"]


   
admin.site.register(Students,StudentsAdmin)
admin.site.register(Classes,ClassesAdmin)

admin.site.register(MyUser, MyUserAdmin)

# admin.site.register(Courses)
# admin.site.register(Years)
