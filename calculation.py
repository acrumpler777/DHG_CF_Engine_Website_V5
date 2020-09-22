import pandas as pd

from DHG_CF_Engine.cash_flow_engine.calculation_cf import *

wp_loan_tape = pd.read_csv("DHG_CF_Engine/media/BankValuationTest.txt", sep='\t', na_values="N/A").fillna("Nothing")

default_final_table_storage, principal_final_table_storage, prepay_final_table_storage, \
        recovery_final_table_storage, interest_final_table_storage, ecf_final_table_storage, dcf_final_table_storage, \
        ci_final_table_storage, ccf_final_table_storage, final_cf_df = calculation_cf(wp_loan_tape=wp_loan_tape)