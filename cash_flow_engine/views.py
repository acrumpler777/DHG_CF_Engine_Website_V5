from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import fileUploadForm
from .models import *
import pandas as pd
from .calculation_cf import *
import numpy as np
import csv
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import ctypes
from tinycc import compile

# Create your views here.
@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'cash_flow_engine/home.html', context)

@login_required(login_url='login')
def dashboard(request):
    try:
        summary = pd.read_csv("media/BankValuationTest.txt_Sum.txt", sep='\t')  # make dynamic with dropdown later
        numberloans = len(summary.index)
        total_ecf = (summary['Expected_Cash_Flows'].sum())
        total_dcf = (summary['PV_Cash_Flows'].sum())
        average_maturity = (summary['Months_To_Maturity'].mean())
        files = fileUpload.objects.all()
        call_code_chart = summary.groupby(['Call_Code'])['Expected_Cash_Flows', 'PV_Cash_Flows'].sum().reset_index()
        call_code_chart = call_code_chart.round(decimals=2)

        pd.options.display.float_format = '${:,.2f}'.format
        call_code = []
        ecf = []
        dcf = []
        for index, row in call_code_chart.iterrows():
            count = -1
            for item in row:
                count += 1
                if count == 0:
                    call_code.append(item)
                if count == 1:
                    ecf.append(item)
                if count == 2:
                    dcf.append(item)

    except:
        summary = 0
        numberloans = "N/A"
        total_ecf = "N/A"
        total_dcf = "N/A"
        average_maturity = "N/A"
        files = fileUpload.objects.all()
        call_code = []
        ecf = []
        dcf = []




    context = {'numberloans':numberloans,
               'total_ecf':total_ecf,
               'total_dcf':total_dcf,
               'average_maturity':average_maturity,
               'files':files,
               'call_code':call_code,
               'ecf':ecf,
               'dcf':dcf}
    return render(request, 'cash_flow_engine/dashboard.html', context)


@login_required(login_url='login')
def table(request):
    try:
        summary = pd.read_csv("media/BankValuationTest.txt_Sum.txt", sep='\t')  #make dynamic with dropdown later
        files = fileUpload.objects.all()
    except:
        summary = 0
        files = fileUpload.objects.all()

    context = {'summary':summary,
               'files': files,}
    return render(request, 'cash_flow_engine/table.html', context)

@login_required(login_url='login')
def individualcf(request, pk):
    loan_number = pk
    summary = pd.read_csv("media/BankValuationTest.txt_Output.txt", sep='\t')  # make dynamic later
    cashflow = summary[summary['Note_Number']==pk]

    context = {'loan_number':loan_number,
               'cashflow':cashflow,}
    return render(request, 'cash_flow_engine/individualcf.html', context)

@login_required(login_url='login')
def exportportfolio(request):
    response = HttpResponse(content_type='text')
    response['Content-Disposition'] = 'attachment; filename="Loan_Summary.txt"'

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Note_Number', 'Call_Code', 'Months_To_Maturity','Expected_Cash_Flows','PV_Cash_Flows'])

    summary = pd.read_csv("media/BankValuationTest.txt_Sum.txt", sep='\t')  # make dynamic later
    summary.drop(summary.columns[len(summary.columns) - 1], axis=1, inplace=True) # temporary fix, make better later

    for row in summary.values:
        writer.writerows([row])

    return response

@login_required(login_url='login')
def exportindividualcf(request, pk):
    response = HttpResponse(content_type='text')
    response['Content-Disposition'] = 'attachment; filename="Individual_CF.txt"'

    writer = csv.writer(response, delimiter='\t')
    writer.writerow(['Note_Number', 'Borrower_Name', 'Acquired_Bank', 'FDIC_Asset_Pool', 'Pool', 'Subpool', 'Accounting_Treatment',
                         'Accrual_Status', 'Individually_Reviewed', 'Payment_Type',
                         'Coupon_Type', 'SMM', 'Valuation_Approach', 'Coupon',
                         'Call_Code', 'Lifetime_Floor', 'Discount_Rate', 'Next_Reset_Coupon', 'Legal_Balance_Initial',
                         'Bank_Balance_Initial', 'Monthly_CDR_Cohorts', 'Months_To_Next Rate_Reset',
                         'Months_To_Maturity','Loss_Given_Default', 'Recovery_Lag', 'Amortization_Term', 'Discount_Amortization_Method',
                         'Specific_Impairment', 'Recorded_Investment', 'Cohort', 'Period','Contractual_Beginning_Principal', 'Expected_Beginning_Principal',
                         'Expected_Default','Contractual_Principal', 'Expected_Principal','Interest_Rate', 'Contractual_Interest',
                         'Expected_Interest', 'Contractual_Prepaid_Principal',
                          'Expected_Prepaid_Principal',
                         'Contractual_Ending_Principal', 'Expected_Ending_Principal', 'Recovery',
                         'Contractual_Cash_Flows',
                         'Expected_Cash_Flows', 'PV_Cash_Flows'])

    summary = pd.read_csv("media/BankValuationTest.txt_Output.txt", sep='\t')  # make dynamic later

    cashflow = summary[summary['Note_Number'] == pk]
    for row in cashflow.values:
        writer.writerows([row])

    return response


@login_required(login_url='login')
def loanupload(request):
    if request.method == 'POST':
        form = fileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            filetxt = form.cleaned_data['filetxt']
            #dll_path = compile("cash_flow_engine/calculation.c")
            _libfib = ctypes.CDLL('cash_flow_engine/calculation.dll')  #Todo fix error here in website

            def c_calculation():
                return _libfib.main(ctypes.c_int())

            c_calculation()

            # wp_loan_tape = pd.read_csv("media/"+str(filetxt), sep='\t', na_values="N/A").fillna(
            #     "Nothing")

            # final_cf_df, sum_cf_df = calculation_cf(wp_loan_tape=wp_loan_tape)

            # final_cf_df.to_csv("media/"+str(filetxt)+"_Output.txt", header=True, index=None, sep='\t', mode='a')
            # sum_cf_df.to_csv("media/"+str(filetxt)+"_Sum.txt", header=True, index=None, sep='\t', mode='a')

            edit = fileUpload.objects.get(filetxt=filetxt)
            edit.calculated_file = str(filetxt)+"_Output.txt"
            edit.sum_file = str(filetxt)+"_Sum.txt"
            edit.save()

            return redirect("loanupload")
    else:
        form = fileUploadForm()
    files = fileUpload.objects.all()
    context = {'form': form,
               'files': files,}
    return render(request, 'cash_flow_engine/loanupload.html', context)


def delete_file(request, pk):
    if request.method == 'POST':
        file = fileUpload.objects.get(pk=pk)
        file.delete()
    return redirect("loanupload")




@login_required(login_url='login')
def documentation(request):
    context = {}
    return render(request, 'cash_flow_engine/documentation.html', context)

