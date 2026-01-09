from django.db import models


class registerr(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)

class uploads(models.Model):
    u_id = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    married = models.CharField(max_length=50)
    dependents = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    self_employed = models.CharField(max_length=50)
    applicant_income = models.IntegerField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField()
    loan_amount_term = models.FloatField()
    credit_history = models.CharField(max_length=50)
    property_area = models.CharField(max_length=50)
    result = models.CharField(max_length=150)
    result_prob = models.CharField(max_length=150)
    status = models.CharField(max_length=150)

class loan_application(models.Model):
    u_id = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    married = models.CharField(max_length=50)
    dependents = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    self_employed = models.CharField(max_length=50)
    applicant_income = models.IntegerField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField()
    loan_amount_term = models.FloatField()
    credit_history = models.CharField(max_length=50)
    property_area = models.CharField(max_length=50)
    result = models.CharField(max_length=150)
    result_prob = models.CharField(max_length=150)
    application_status = models.CharField(max_length=150, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)

class staff(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)