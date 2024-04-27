from django.urls import path
from . import views

#app_name = "polls"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('AllStudents/<int:id>/', views.AllStudents, name='AllStudents'),
    path('AllClasses/', views.AllClasses, name='AllClasses'),
    path('search_student_autocomplete/', views.search_student_autocomplete, name='search_student_autocomplete'),

    path('StudentDetailPage/<int:id>/', views.StudentDetailPage, name='StudentDetailPage'),
    path('ReceiveStudentFee/<int:id>/', views.ReceiveStudentFee, name='ReceiveStudentFee'),

    path('AddNewStudent/', views.AddNewStudent, name='AddNewStudent'),
    path('UpdateStudent/<int:id>/', views.UpdateStudent, name='UpdateStudent'),
    path('DeleteStudent/<int:id>/', views.DeleteStudent, name='DeleteStudent'),


    path('AllPaidStudents/', views.AllPaidStudents, name='AllPaidStudents'),
    path('AllUnPaidStudents/', views.AllUnPaidStudents, name='AllUnPaidStudents'),
        
]
