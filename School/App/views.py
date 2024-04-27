from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import *
from .forms import *
from django.http import HttpResponse
from datetime import datetime, timedelta
import pyotp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
import os
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#C:\Users\DIMOSO JR\Desktop\ProjectWork\SmartInvigilation\SmartInvigilationProject\SmartInvigilationApp
print(BASE_DIR)
from django.core.files.base import ContentFile


#@login_required(login_url='login')
def home(request):
    

    return render(request,'App/home.html')









#@login_required(login_url='login')
def AllClasses(request):
    classes = Classes.objects.all()

    context = {
        "classes":classes,
    }

    return render(request,'App/AllClasses.html',context)


@login_required(login_url='login')
def AllStudents(request, id):
    classId = Classes.objects.get(id=id)
    className = classId.ClassName

    form = StudentsSearchForm(request.POST or None)
    x= datetime.now()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(

            Class__id__icontains = classId.id,

        ).order_by('-id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        "current_date":current_date,
        "className":className,
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        Class__id__icontains = classId.id,

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.all()
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="List oF Students.csv"'
            writer = csv.writer(response)
            writer.writerow(['Class', 'Student Name', 'Status Fee'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.Class,student.StudentName,student.StatusFee])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        "className":className,
    }   

    return render(request, 'App/AllStudents.html',context)



@login_required(login_url='login')
def search_student_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StudentName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = Students.objects.filter(search)
    mylist= []
    mylist += [x.StudentName for x in filters]
    return JsonResponse(mylist, safe=False)






def StudentDetailPage(request, id):
    queryset = Students.objects.get(id=id)
    
    context ={
        
        "queryset":queryset
    }
    
    
        

    return render(request, 'App/StudentDetailPage.html',context)


def ReceiveStudentFee(request, id):
    queryset = Students.objects.get(id=id)
    studentId = queryset.id
    

    form= ReceiveStudentFeeeForm(request.POST or None, instance=queryset)

    if form.is_valid():
    
        instance = form.save(commit=False)
        instance.StatusFee += instance.ReceivedAmount
        instance.AmountRemained = instance.Class.ClassFee - instance.StatusFee
        instance.AmountExceed = instance.StatusFee - instance.Class.ClassFee
        instance.ReceivedBy = request.user.username

        Total_amount_paid = instance.StatusFee
        amount_remained = instance.AmountRemained
        amount_exceed = instance.AmountExceed
        total_fee = instance.Class.ClassFee

        if Total_amount_paid == total_fee:
            instance.is_finished = True
            instance.save()

        #messages.success(request,"Items Issued successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in store")
        instance.save()
        messages.success(request, "Received successfully. " + "Tsh. " + str(instance.ReceivedAmount) + " " + str(instance.StudentName) + "/=")
        #return redirect('stock_detailpage/'+str(instance.id))
        return redirect('StudentDetailPage',id=id)
        #return HttpResponseRedirect(instance.get_absolute_url())
    context ={
        "instance":queryset,
        "form":form,
        "studentId":studentId,

        # "Total_amount_paid":Total_amount_paid,
        # "amount_remained":amount_remained,
        # "amount_exceed":amount_exceed,
        
        #"username": 'Issued By: ' + str(request.user),
        "title": 'Receive ' + str(queryset.StudentName),
    }
    
    
        

    return render(request, 'App/ReceiveStudentFee.html',context)







# class add_items(SuccessMessageMixin, CreateView):
#     model = Stock
#     template_name = 'App/AddNewStudent.html'
#     form_class = StudentCreateForm
#     success_url = reverse_lazy('AddNewStudent')
#     success_message = "Item added successfully in your stock"
# class update_items(SuccessMessageMixin, UpdateView):
#     model = Stock
#     template_name = 'DimosoApp/add_items.html'
#     form_class = StockUpdateForm
#     success_url = reverse_lazy('stock')
#     success_message = "Item updated successfully in your stock"


def AddNewStudent(request):
    form = StudentCreateForm()
    if request.method == "POST":
        StudentName = request.POST.get('StudentName')
        form = StudentCreateForm(request.POST or None, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {StudentName} were added successfully")
            return redirect('AddNewStudent')

        messages.success(request, f"Error adding new student")
        return redirect('AddNewStudent')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/AddNewStudent.html',context)


def UpdateStudent(request,id):
    x = Students.objects.get(id=id)
    form = StudentCreateForm(instance=x)
    if request.method == "POST":
        StudentName = request.POST.get('StudentName')
        form = StudentCreateForm(request.POST, files=request.FILES, instance=x)

        if form.is_valid():
            form.save()
            messages.success(request, f"Informations of {x.StudentName} were updated successfully")
            return redirect('AllClasses')

        messages.success(request, f"Error adding new student")
        return redirect('AllClasses')


    context ={
        
        "form":form,
        
    }
    
    
        

    return render(request, 'App/UpdateStudent.html',context)



def DeleteStudent(request,id):
    x = Students.objects.get(id=id)
    x.delete()
    messages.success(request, f"Informations of {x.StudentName} were deleted successfully")
    return redirect('AllClasses')
    
    
    
        













@login_required(login_url='login')
def AllPaidStudents(request):
    # classId = Classes.objects.get(id=id)
    # className = classId.ClassName

    form = StudentsSearchForm(request.POST or None)
    x= datetime.now()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(

            is_finished = True

        ).order_by('-id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        "current_date":current_date,
        
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        is_finished = True

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.all()
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="List oF Students.csv"'
            writer = csv.writer(response)
            writer.writerow(['Class', 'Student Name', 'Status Fee'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.Class,student.StudentName,student.StatusFee])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        
    }   

    return render(request, 'App/AllPaidStudents.html',context)
    





@login_required(login_url='login')
def AllUnPaidStudents(request):
    # classId = Classes.objects.get(id=id)
    # className = classId.ClassName

    form = StudentsSearchForm(request.POST or None)
    x= datetime.now()
    current_date = x.strftime('%d-%m-%Y %H:%M')
    

    queryset = Students.objects.filter(
            is_finished = False

            

        ).order_by('-id')


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)
    
    form = StudentsSearchForm(request.POST or None)




    #MWISHO HAP




    context ={
        "queryset":queryset,
        "form":form,
        "page":page,
        "current_date":current_date,
        
    }

    #kwa ajili ya kufilter items and category ktk form
    if request.method == 'POST':
        #category__icontains=form['category'].value(),
        Class = form['Class'].value()

        

                                        
        queryset = Students.objects.filter(
                                        StudentName__icontains=form['StudentName'].value(),
                                        is_finished = False

                                        #last_updated__gte=form['start_date'].value(),
                                        # last_updated__lte=form['end_date'].value()
                                        #last_updated__range=[
                                            #form['start_date'].value(),
                                            #form['end_date'].value()
                                        #]
            )
        if (Class != ''):
            queryset = Students.objects.all()
            queryset = queryset.filter(Class_id=Class)

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)
            #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI
        
        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="List oF Students.csv"'
            writer = csv.writer(response)
            writer.writerow(['Class', 'Student Name', 'Status Fee'])
            instance = queryset
            for student in queryset:
                writer.writerow([student.Class,student.StudentName,student.StatusFee])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

            #HII NI CONTEXT KWA AJILI YA KUSEARCH ITEM OR CATEGORY KWENYE FORMYETU
        context ={
        #"QuerySet":QuerySet,
        "form":form,
        "queryset":queryset,
        "page":page,
        
    }   

    return render(request, 'App/AllUnPaidStudents.html',context)