#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
import joblib


scaler = joblib.load("./ML/scaler_minmax.joblib")
model = joblib.load("./ML/rf_model.joblib")


def predict(data):
    test_data = pd.DataFrame({'Gender':[int(data['Gender'][0])],
                              'Married':[int(data['Married'][0])],
                              'Dependents':[str(data['Dependents'][0])],
                              'Education':[int(data['Education'][0])],
                              'Self_Employed':[int(data['Self_Employed'][0])],
                              'ApplicantIncome':[int(data['ApplicantIncome'][0])],
                              'CoapplicantIncome':[int(data['CoapplicantIncome'][0])],
                              'LoanAmount':[int(data['LoanAmount'][0])],
                              'Loan_Amount_Term':[int(data['Loan_Amount_Term'][0])],
                              'Credit_History':[int(data['Credit_History'][0])],
                              'Property_Area':[int(data['Property_Area'][0])],
                                })
    columns_to_normalize = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
    test_data[columns_to_normalize] = scaler.transform(test_data[columns_to_normalize])
    print("Test Data:",test_data)
    pred=model.predict(test_data)
    pred_proba = str(int(model.predict_proba(test_data)[0][1]*100))
    print("Result probability: ",pred_proba)
    print("Result: ",pred)
    res_proba = pred_proba# [0:5]
    return res_proba,pred[0]



#pred = predict(test_data)
#print(pred)

