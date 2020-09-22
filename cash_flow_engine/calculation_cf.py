import pandas as pd


def calculation_cf(wp_loan_tape):
    # Data frame storage
    # wp_loan_tape = pd.read_csv("DHG_CF_Engine/media/BankValuationTest.txt", sep='\t', na_values="N/A").fillna(
    #     "Nothing")
    final_cf_df = pd.DataFrame([])

    # Loop through individual rows from imported data frame and store relevant variables
    num_rows = len(wp_loan_tape.index)
    row_count = 0
    while row_count < (num_rows - 0):  # The number here will be 0 when in use (i.e., not testing)
        note_number = wp_loan_tape.iloc[row_count, 0]
        borrower_name = wp_loan_tape.iloc[row_count, 1]
        acquired_bank = wp_loan_tape.iloc[row_count, 2]
        fdic_asset_pool = wp_loan_tape.iloc[row_count, 3]
        pool = wp_loan_tape.iloc[row_count, 4]
        subpool = wp_loan_tape.iloc[row_count, 5]
        accounting_treatment = wp_loan_tape.iloc[row_count, 6]
        accrual_status = wp_loan_tape.iloc[row_count, 7]
        individually_reviewed = wp_loan_tape.iloc[row_count, 8]
        payment_type = wp_loan_tape.iloc[row_count, 9]
        coupon_type = wp_loan_tape.iloc[row_count, 10]
        smm = wp_loan_tape.iloc[row_count, 11]
        valuation_approach = wp_loan_tape.iloc[row_count, 12]
        coupon = wp_loan_tape.iloc[row_count, 13]
        call_code = wp_loan_tape.iloc[row_count, 14]
        lifetime_floor = wp_loan_tape.iloc[row_count, 15]
        discount_rate = wp_loan_tape.iloc[row_count, 16]
        next_reset_coupon = wp_loan_tape.iloc[row_count, 17]
        legal_balance_initial = wp_loan_tape.iloc[row_count, 18]
        bank_balance_initial = wp_loan_tape.iloc[row_count, 19]
        monthly_cdr_cohorts_initial = wp_loan_tape.iloc[row_count, 20]  # This may change from engagement to engagement
        months_to_next_rate_reset = wp_loan_tape.iloc[row_count, 21]
        months_to_maturity = wp_loan_tape.iloc[row_count, 22]
        loss_given_default = wp_loan_tape.iloc[row_count, 23]
        recovery_lag = wp_loan_tape.iloc[row_count, 24]
        amortization_term = wp_loan_tape.iloc[row_count, 25]
        discount_amortization_method = wp_loan_tape.iloc[row_count, 26]
        specific_impairment = wp_loan_tape.iloc[row_count, 27]
        recorded_investment = wp_loan_tape.iloc[row_count, 28]
        cohort = wp_loan_tape.iloc[row_count, 29]

        # Large if statement to determine CDR
        monthly_cdr_cohorts = 0
        if accrual_status == "Accrual" and specific_impairment > 0:  # TODO criteria not yet tested and will want -1
            # to be smaller in use below after tested
            while (specific_impairment - (bank_balance_initial * monthly_cdr_cohorts_initial)) < -1 or (
                    specific_impairment - (bank_balance_initial * monthly_cdr_cohorts_initial)) > 1:
                cf_df = pd.DataFrame([])

                count = 0
                while count < months_to_maturity:
                    period = count + 1
                    if count == 0:
                        legal_balance = legal_balance_initial
                    else:
                        legal_balance = float(cf_df['Contractual_Ending_Principal'].tail(
                            1))  # ending principal is the same for legal and bank need to chage
                    if count == 0:
                        bank_balance = bank_balance_initial
                    else:
                        bank_balance = float(cf_df['Expected_Ending_Principal'].tail(1))
                    if wp_loan_tape.columns.values[20] == "Expected_Default":
                        expected_default = monthly_cdr_cohorts_initial
                    else:
                        expected_default = bank_balance * monthly_cdr_cohorts_initial
                    if coupon_type == "Fixed":
                        period_coupon = coupon
                    else:
                        if period >= months_to_next_rate_reset:
                            alternate_coupon = next_reset_coupon
                            period_coupon = max(alternate_coupon, lifetime_floor)
                        else:
                            alternate_coupon = coupon
                            period_coupon = max(alternate_coupon, lifetime_floor)
                    contractual_interest = legal_balance * (period_coupon / 12)
                    expected_interest = (bank_balance - expected_default) * (period_coupon / 12)
                    if months_to_maturity == period:
                        contractual_principal = legal_balance
                        expected_principal = bank_balance - expected_default
                    elif legal_balance == 0 or payment_type == "IO" or period > months_to_maturity or \
                            accrual_status == "Non-Accrual":
                        contractual_principal = 0
                        expected_principal = 0
                    else:
                        contractual_principal = min(max((legal_balance * ((period_coupon / 12 * (pow((1 +
                                                    (period_coupon / 12)), max(1, amortization_term - period + 1)))) / (
                                                    (pow((1 + (period_coupon / 12)), max(1, amortization_term -
                                                    period + 1))) - 1))) - (legal_balance * (period_coupon / 12)), 0),
                                                    legal_balance)
                        expected_principal = min(max(((bank_balance - expected_default) * ((period_coupon / 12 * (
                                                pow((1 + (period_coupon / 12)), max(1, amortization_term - period + 1))
                                                )) / ((pow((1 + (period_coupon / 12)), max(1, amortization_term -
                                                period + 1))) - 1))) - ((bank_balance - expected_default) * (
                                                period_coupon / 12)), 0), (bank_balance - expected_default))

                    prepaid_principal_contractual = (legal_balance - contractual_principal) * smm
                    prepaid_principal_expected = (bank_balance - expected_default - expected_principal) * smm
                    contractual_ending_principal = (
                            legal_balance - contractual_principal - prepaid_principal_contractual)
                    expected_ending_principal = (
                            bank_balance - expected_default - expected_principal - prepaid_principal_expected)
                    recovery = 0  # Build into when we get a loan to test
                    contractual_cash_flows = (
                            contractual_principal + contractual_interest + prepaid_principal_contractual)
                    expected_cash_flows = (expected_principal + expected_interest + prepaid_principal_expected)
                    pv_of_cash_flows = expected_cash_flows / ((1 + (discount_rate / 12)) ** period)

                    # Append period CF
                    append_df = pd.DataFrame(
                        [[period, legal_balance, bank_balance, expected_default, contractual_principal,
                          expected_principal,
                          period_coupon, contractual_interest, expected_interest, prepaid_principal_contractual,
                          prepaid_principal_expected, contractual_ending_principal, expected_ending_principal, recovery,
                          contractual_cash_flows, expected_cash_flows, pv_of_cash_flows]],
                        columns=['Period', 'Contractual_Beginning_Principal', 'Expected_Beginning_Principal',
                             'Expected_Default',
                             'Contractual_Principal', 'Expected_Principal', 'Interest_Rate', 'Contractual_Interest',
                             'Expected_Interest', 'Contractual_Prepaid_Principal', 'Expected_Prepaid_Principal',
                             'Contractual_Ending_Principal', 'Expected_Ending_Principal', 'Recovery',
                             'Contractual_Cash_Flows',
                             'Expected_Cash_Flows', 'PV_Cash_Flows'])
                    cf_df = cf_df.append(append_df, ignore_index=True)
                    count += 1
                if (specific_impairment - (bank_balance_initial * monthly_cdr_cohorts_initial)) < -1:
                    monthly_cdr_cohorts_initial = monthly_cdr_cohorts_initial - .001
                else:
                    monthly_cdr_cohorts_initial = monthly_cdr_cohorts_initial + .001
        elif accrual_status == "Non-Accrual" and accounting_treatment == "ASC 310-30":
            monthly_cdr_cohorts = 1
        elif accrual_status == "Accrual" and accounting_treatment == "ASC 310-10":
            monthly_cdr_cohorts = monthly_cdr_cohorts_initial
        else:
            monthly_cdr_cohorts = monthly_cdr_cohorts_initial

        # Individual loans cf data frame storage
        cf_df = pd.DataFrame([])

        # Loop through individual loan terms and calculate cfs
        count = 0
        while count < months_to_maturity:
            period = count + 1

            # Legal and bank balance conditional statement
            if count == 0:
                legal_balance = legal_balance_initial
                bank_balance = bank_balance_initial
            else:
                legal_balance = float(cf_df['Contractual_Ending_Principal'].tail(1))
                bank_balance = float(cf_df['Expected_Ending_Principal'].tail(1))

            expected_default = monthly_cdr_cohorts_initial
            # Expected default conditional statement
            # if wp_loan_tape.columns.values[20] == "Expected Default":
            #     expected_default = monthly_cdr_cohorts_initial
            # else:
            #     expected_default = bank_balance * monthly_cdr_cohorts

            # Coupon conditional statement
            if coupon_type == "Fixed":
                period_coupon = coupon
            else:
                if months_to_next_rate_reset != "Nothing":
                    if period >= months_to_next_rate_reset:
                        alternate_coupon = next_reset_coupon
                        period_coupon = max(alternate_coupon, lifetime_floor)
                    else:
                        alternate_coupon = coupon
                        period_coupon = max(alternate_coupon, float(lifetime_floor))

                else:
                    alternate_coupon = coupon
                    period_coupon = max(alternate_coupon, lifetime_floor)


            # CF calculations with various conditional statements
            contractual_interest = legal_balance * (period_coupon / 12)
            expected_interest = (bank_balance - expected_default) * (period_coupon / 12)
            if months_to_maturity == period:
                contractual_principal = legal_balance
                expected_principal = bank_balance - expected_default
            elif legal_balance == 0 or payment_type == "IO" or period > months_to_maturity or accrual_status == \
                    "Non-Accrual":
                contractual_principal = 0
                expected_principal = 0
            else:
                contractual_principal = min(max((legal_balance * ((period_coupon / 12 * (pow((1 + (period_coupon / 12)),
                                            max(1, amortization_term - period + 1)))) / ((pow((1 + (period_coupon / 12)
                                            ), max(1, amortization_term - period + 1))) - 1))) -
                                            (legal_balance * (period_coupon / 12)), 0), legal_balance)
                expected_principal = min(max(((bank_balance - expected_default) * ((period_coupon / 12 * (
                                        pow((1 + (period_coupon / 12)), max(1, amortization_term - period + 1))
                                        )) / ((pow((1 + (period_coupon / 12)), max(1, amortization_term -
                                        period + 1))) - 1))) - ((bank_balance - expected_default) * (
                                        period_coupon / 12)), 0), (bank_balance - expected_default))

            prepaid_principal_contractual = (legal_balance - contractual_principal) * smm
            prepaid_principal_expected = (bank_balance - expected_default - expected_principal) * smm
            contractual_ending_principal = (legal_balance - contractual_principal - prepaid_principal_contractual)
            expected_ending_principal = (bank_balance - expected_default - expected_principal -
                                         prepaid_principal_expected)
            recovery = 0  # Todo Build into when we get a loan to test
            contractual_cash_flows = (contractual_principal + contractual_interest + prepaid_principal_contractual)

            if individually_reviewed == 1:
                expected_cash_flows = bank_balance * (1 - loss_given_default)
                pv_of_cash_flows = expected_cash_flows
            else:
                expected_cash_flows = (expected_principal + expected_interest + prepaid_principal_expected)
                pv_of_cash_flows = expected_cash_flows / ((1 + (discount_rate / 12)) ** period)

            # Append period CF
            append_df = pd.DataFrame(
                [[note_number, borrower_name, acquired_bank, fdic_asset_pool, pool, subpool, accounting_treatment, accrual_status,
                  individually_reviewed, payment_type, coupon_type, smm, valuation_approach, coupon, call_code,
                  lifetime_floor, discount_rate,next_reset_coupon,legal_balance_initial,
                  bank_balance_initial,monthly_cdr_cohorts,months_to_next_rate_reset,months_to_maturity,
                  loss_given_default,recovery_lag,amortization_term, discount_amortization_method,
                  specific_impairment, recorded_investment, cohort,period,legal_balance, bank_balance,expected_default,
                  contractual_principal, expected_principal,period_coupon, contractual_interest, expected_interest, prepaid_principal_contractual,
                  prepaid_principal_expected, contractual_ending_principal, expected_ending_principal, recovery,
                  contractual_cash_flows, expected_cash_flows, pv_of_cash_flows]],
                columns=['Note_Number', 'Borrower_Name', 'Acquired_Bank', 'FDIC_Asset_Pool', 'Pool', 'Subpool', 'Accounting_Treatment',
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
            cf_df = cf_df.append(append_df, ignore_index=True)

            count += 1

        # Concatenations to store individual cfs into main storage
        final_cf_df = final_cf_df.append(cf_df, ignore_index=True)
        row_count += 1

    sum_cf_df = final_cf_df.groupby(['Note_Number','Call_Code','Months_To_Maturity'])['Expected_Cash_Flows', 'PV_Cash_Flows'].sum().reset_index()

    return final_cf_df, sum_cf_df