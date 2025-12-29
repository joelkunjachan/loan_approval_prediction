"""genderclassification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.first),
    path('index',views.index),
    path('register/',views.register),
    path('register/registration',views.registration),
    # path('s_register',views.s_register),
    #path('s_registration',views.s_registration),  
    path('login/',views.login),    
    path('logout/',views.logout),    
    path('login/addlogin',views.addlogin),    
    path('loan_eligibility/',views.loan_eligibility),    
    path('loan_eligibility/check_eligibility',views.check_eligibility),    
    #path('addqsan',views.addqsan),    
    #path('v_qst',views.v_qst), 
    path('v_tchr',views.v_tchr), 
    #path('v_stdnt',views.v_stdnt), 
    #path('answer/<int:id>',views.answer),   
    #path('answer/addanswer',views.addanswer),   

  
    
    
]
