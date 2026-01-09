from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
import datetime

from .models import *

from ML import loan_prediction

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=registerr(name=name,email=email,password=password)
        reg.save()
        return render(request,'index.html')
    
def s_register(request):
    return render(request,'s_register.html')

def s_registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=staff(name=name,email=email,password=password)
        reg.save()
        return render(request,'index.html')
    
def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif registerr.objects.filter(email=email,password=password).exists():
        userdetails=registerr.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['tid'] = userdetails.id
        

            return render(request,'index.html')

    elif staff.objects.filter(email=email,password=password).exists():
        userdetails=staff.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['sid'] = userdetails.id
        

            return render(request,'index.html')

    else:
        return render(request, 'login.html')
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)

    
def loan_eligibility(request):
    return render(request,'loan_eligibility.html')

def check_eligibility(request):
    if request.method=="POST":
        u_id = str(request.session['tid'])
        data = dict(request.POST)
        result_prob, result = loan_prediction.predict(data)

         # Mappings for reverse conversion
        gender_map = {'1': 'Male', '0': 'Female'}
        married_map = {'1': 'Yes', '0': 'No'}
        education_map = {'1': 'Graduate', '0': 'Not Graduate'}
        self_employed_map = {'1': 'Yes', '0': 'No'}
        credit_history_map = {'1': 'Yes', '0': 'No'}
        property_area_map = {
            '0': 'Rural',
            '1': 'Semiurban',
            '2': 'Urban'
        }
        # Save to DB
        uploads.objects.create(
            u_id=u_id,
            gender=gender_map.get(data['Gender'][0], 'Unknown'),
            married=married_map.get(data['Married'][0], 'Unknown'),
            dependents=data['Dependents'][0],
            education=education_map.get(data['Education'][0], 'Unknown'),
            self_employed=self_employed_map.get(data['Self_Employed'][0], 'Unknown'),
            applicant_income=int(data['ApplicantIncome'][0]),
            coapplicant_income=float(data['CoapplicantIncome'][0]),
            loan_amount=float(data['LoanAmount'][0]),
            loan_amount_term=float(data['Loan_Amount_Term'][0]),
            credit_history=credit_history_map.get(data['Credit_History'][0], 'Unknown'),
            property_area=property_area_map.get(data['Property_Area'][0], 'Unknown'),
            result_prob=str(result_prob),
            result=str(result),
            status=str("not_applied")
        )
        return render(request,'loan_eligibility.html',{'result':int(result_prob)})
    return render(request,'loan_eligibility.html')

# def addqsan(request):
#     if request.method=="POST":
        
#         answer=request.POST.get('answer')
#         t_id=request.session['tid']

#         reg=que_ans(question='question',answer=answer,t_id=t_id)
#         reg.save()
#         return render(request,'index.html')
    

# def v_qst(request):
#     user = que_ans.objects.all()
#     return render(request,'v_question.html', {'result': user})

# def answer(request,id):
#     data=que_ans.objects.get(id=id)
#     return render(request,'answer.html',{'result':data})

# def addanswer(request):
#     if request.method=="POST":
#         s_id=request.session['sid']
#         q_id=request.POST.get('q_id')
#         answer=request.POST.get('answer')

#         cus=s_answer(s_id=s_id,q_id=q_id,answer=answer)
#         cus.save()
#         return redirect(v_qst)
    

def v_tchr(request):
    user = registerr.objects.all()
    return render(request,'v_teacher.html', {'result': user})

def v_applications(request):
    applications = loan_application.objects.all()
    pending_count = applications.filter(application_status='pending').count()
    approved_count = applications.filter(application_status='approved').count()
    rejected_count = applications.filter(application_status='rejected').count()
    return render(request,'v_applications.html', {
        'applications': applications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count
    })

def approve_application(request, id):
    if request.session.get('sid'):
        application = loan_application.objects.get(id=id)
        application.application_status = 'approved'
        application.save()
        return redirect('v_applications')
    else:
        return redirect('login')

def reject_application(request, id):
    if request.session.get('sid'):
        application = loan_application.objects.get(id=id)
        application.application_status = 'rejected'
        application.save()
        return redirect('v_applications')
    else:
        return redirect('login')

def view_loan_application(request):
    if request.session.get('admin'):
        applications = loan_application.objects.all()
        total = applications.count()
        pending = applications.filter(application_status='pending').count()
        approved = applications.filter(application_status='approved').count()
        rejected = applications.filter(application_status='rejected').count()
        return render(request, 'view_loan_application.html', {
            'applications': applications,
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected
        })
    else:
        return redirect('login')

def my_loan_application(request):
    u_id = str(request.session.get('tid'))
    if not u_id:
        return redirect('login')
    applications = loan_application.objects.filter(u_id=u_id)
    print("application status:", [app.application_status for app in applications])
    return render(request, 'my_loan_application.html', {'applications': applications})

def apply_loan(request):
    u_id = str(request.session.get('tid'))
    if not u_id:
        return redirect('login')
    if request.method == "POST":
        data = dict(request.POST)
        result_prob, result = loan_prediction.predict(data)

         # Mappings for reverse conversion
        gender_map = {'1': 'Male', '0': 'Female'}
        married_map = {'1': 'Yes', '0': 'No'}
        education_map = {'1': 'Graduate', '0': 'Not Graduate'}
        self_employed_map = {'1': 'Yes', '0': 'No'}
        credit_history_map = {'1': 'Yes', '0': 'No'}
        property_area_map = {
            '0': 'Rural',
            '1': 'Semiurban',
            '2': 'Urban'
        }
        # Save to loan_application
        loan_application.objects.create(
            u_id=u_id,
            gender=gender_map.get(data['Gender'][0], 'Unknown'),
            married=married_map.get(data['Married'][0], 'Unknown'),
            dependents=data['Dependents'][0],
            education=education_map.get(data['Education'][0], 'Unknown'),
            self_employed=self_employed_map.get(data['Self_Employed'][0], 'Unknown'),
            applicant_income=int(data['ApplicantIncome'][0]),
            coapplicant_income=float(data['CoapplicantIncome'][0]),
            loan_amount=float(data['LoanAmount'][0]),
            loan_amount_term=float(data['Loan_Amount_Term'][0]),
            credit_history=credit_history_map.get(data['Credit_History'][0], 'Unknown'),
            property_area=property_area_map.get(data['Property_Area'][0], 'Unknown'),
            result_prob=str(result_prob),
            result=str(result),
            application_status='pending'
        )
        return render(request, 'apply_loan.html', {'message': 'Loan application submitted successfully!'})
    return render(request, 'apply_loan.html')