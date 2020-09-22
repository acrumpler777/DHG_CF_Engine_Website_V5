#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


/* Function declarations */
float max(double num1, double num2);
float min(double num1, double num2);


int main()
{
    char Note_Number[100];
    char Borrower_Name[100];
    char Acquired_Bank[100];
    char FDIC_Asset_Pool[100];
    char Pool[100];
    char Subpool[250];
    char Accounting_Treatment[100];
    char Accrual_Status[100];
    int Individually_Reviewed;
    char Payment_Type[100];
    char Coupon_Type[100];
    double SMM;
    char Valuation_Approach[100];
    double Coupon;
    char Call_Code[100];
    double Lifetime_Floor;
    double Discount_Rate;
    double Next_Reset_Coupon; //-100 specifies N/A
    double Legal_Balance_Initial;
    double Bank_Balance_Initial;
    double Monthly_CDR_Cohorts;
    double Months_To_Next_Rate_Reset;
    double Months_to_Maturity;
    int Loss_Given_Default;
    int Recovery_Lag;
    int Amortization_Term;
    char Discount_Amortization_Method[100];
    double Specific_Impairment;
    double Recorded_Investment;
    char Cohort[400];

    //fscanf(file_pointer, "format string", lost of address of variables)
    FILE *inFile = fopen("media/BankValuationTest.txt", "r");
    FILE *outFile = fopen("media/BankValuationTest.txt_Output.txt", "w");
    FILE *sumFile = fopen("media/BankValuationTest.txt_Sum.txt", "w");

    fprintf(outFile, "Note_Number\tBorrower_Name\tAcquired_Bank\tFDIC_Asset_Pool\tPool\tSubpool\tAccounting_Treatment\tAccrual_Status\tIndividually_Reviewed\tPayment_Type\tCoupon_Type\tSMM\tValuation_Approach\tCoupon\tCall_Code\tLifetime_Floor\tDiscount_Rate\tNext_Reset_Coupon\tLegal_Balance_Initial\tBank_Balance_Initial\tMonthly_CDR_Cohorts\tMonths_To_Next_Rate_Reset\tMonths_to_Maturity\tLoss_Given_Default\tRecovery_Lag\tAmortization_Term\tDiscount_Amortization_Method\tSpecific_Impairment\tRecorded_Investment\tCohort\tPeriod\tContractual_Beginning_Principal\tExpected_Beginning_Principal\tExpected_Default\tContractual_Principal\tExpected_Principal\tInterest_Rate\tContractual_Interest\tExpected_Interest\tContractual_Prepaid_Principal\tExpected_Prepaid_Principal\tContractual_Ending_Principal\tExpected_Ending_Principal\tRecovery\tContractual_Cash_Flows\tExpected_Cash_Flows\tPV_of_Cash_Flows\n");
    fprintf(sumFile, "Note_Number\tCall_Code\tMonths_To_Maturity\tExpected_Cash_Flows\tPV_Cash_Flows\t\n");

    //import file, run calculations and output
    if(inFile == NULL){
        printf("Unable to open the file\n");
    } else {
        while(fscanf(inFile, "%s %s %s %s %s %s %s %s %d %s %s %lf %s %lf %s %lf %lf %lf %lf %lf %lf %lf %lf %d %d %d %s %lf %lf %s",
              Note_Number, Borrower_Name, Acquired_Bank, FDIC_Asset_Pool, Pool, Subpool, Accounting_Treatment,
              Accrual_Status, &Individually_Reviewed, Payment_Type, Coupon_Type, &SMM, Valuation_Approach,
              &Coupon, Call_Code, &Lifetime_Floor, &Discount_Rate, &Next_Reset_Coupon, &Legal_Balance_Initial,
              &Bank_Balance_Initial, &Monthly_CDR_Cohorts, &Months_To_Next_Rate_Reset, &Months_to_Maturity,
              &Loss_Given_Default, &Recovery_Lag, &Amortization_Term, Discount_Amortization_Method,
              &Specific_Impairment, &Recorded_Investment, Cohort)!= EOF){

            //printf("%s %s %s %s %s %s %s %s %d %s %s %lf %s %lf %s %lf %lf %lf %lf %lf %lf %lf %lf %d %d %d %s %lf %lf %s\n",
              //Note_Number, Borrower_Name, Acquired_Bank, FDIC_Asset_Pool, Pool, Subpool, Accounting_Treatment,
              //Accrual_Status, Individually_Reviewed, Payment_Type, Coupon_Type, SMM, Valuation_Approach,
              //Coupon, Call_Code, Lifetime_Floor, Discount_Rate, Next_Reset_Coupon, Legal_Balance_Initial,
              //Bank_Balance_Initial, Monthly_CDR_Cohorts, Months_To_Next_Rate_Reset, Months_to_Maturity,
              //Loss_Given_Default, Recovery_Lag, Amortization_Term, Discount_Amortization_Method,
              //Specific_Impairment, Recorded_Investment, Cohort);

            int count = 0;

            double PVCFSum = 0;
            double ECFSum = 0;

            double Expected_Cash_Flows = 0;
            double Contractual_Ending_Principal = 0;
            double Expected_Ending_Principal = 0;
            while(count < Months_to_Maturity){
                    double Period = count + 1;
                    double Legal_Balance = 0;
                    if(count == 0){
                        Legal_Balance = Legal_Balance_Initial;
                    } else {
                        Legal_Balance = Contractual_Ending_Principal;
                    }
                    double Bank_Balance = 0;
                    if(count == 0){
                        Bank_Balance = Bank_Balance_Initial;
                    } else {
                        Bank_Balance = Expected_Ending_Principal;
                    }
                    double Expected_Default = Bank_Balance * Monthly_CDR_Cohorts; //add if statement here later if needed
                    double Period_Coupon = 0;
                    if(strcmp(Coupon_Type,"Fixed")==0){
                            Period_Coupon = Coupon;
                    } else {
                        double Alternate_Coupon = 0;
                        if(Period >= Months_To_Next_Rate_Reset){
                            Alternate_Coupon = Next_Reset_Coupon;
                            Period_Coupon = max(Alternate_Coupon,Lifetime_Floor);
                        } else {
                            Alternate_Coupon = Coupon;
                            Period_Coupon = max(Alternate_Coupon,Lifetime_Floor);
                        }
                        }
                    double Contractual_Interest = Legal_Balance * (Period_Coupon / 12);
                    double Expected_Interest = (Bank_Balance - Expected_Default) * (Period_Coupon / 12);
                    double Contractual_Principal = 0;
                    double Expected_Principal = 0;
                    if(Months_to_Maturity == Period){
                        Contractual_Principal = Legal_Balance;
                        Expected_Principal = Bank_Balance - Expected_Default;
                    } else if(Legal_Balance == 0 || Payment_Type == "IO" || Period > Months_to_Maturity || Accrual_Status == "Non-Accrual") {
                        Contractual_Principal = 0;
                        Expected_Principal = 0;
                    } else {
                        Contractual_Principal = min(max((Legal_Balance*(((Period_Coupon) / 12*(pow((1+(Period_Coupon / 12)),max(1,Amortization_Term-Period+1))))/
                       ((pow((1+(Period_Coupon / 12)),max(1,Amortization_Term-Period+1)))-1)))-(Legal_Balance*(Period_Coupon / 12)),0), Legal_Balance);

                        Expected_Principal = min(max(((Bank_Balance - Expected_Default)*(((Period_Coupon) / 12*(pow((1+(Period_Coupon / 12)),max(1,Amortization_Term-Period+1))))/
                       ((pow((1+(Period_Coupon / 12)),max(1,Amortization_Term-Period+1)))-1)))-((Bank_Balance - Expected_Default)*(Period_Coupon / 12)),0), (Bank_Balance - Expected_Default));
                    }
                    double Prepaid_Principal_Contractual = (Legal_Balance - Contractual_Principal) * SMM;
                    double Prepaid_Principal_Expected = (Bank_Balance - Expected_Default - Expected_Principal) * SMM;
                    Contractual_Ending_Principal = (Legal_Balance - Contractual_Principal - Prepaid_Principal_Contractual);
                    Expected_Ending_Principal = (Bank_Balance - Expected_Default - Expected_Principal - Prepaid_Principal_Expected);
                    double Recovery = 0; //Build into when we get a loan to test
                    double Contractual_Cash_Flows = (Contractual_Principal + Contractual_Interest + Prepaid_Principal_Contractual);
                    double Expected_Cash_Flows = (Expected_Principal + Expected_Interest + Prepaid_Principal_Expected);
                    ECFSum = Expected_Cash_Flows + ECFSum;
                    double PV_of_Cash_Flows = (Expected_Cash_Flows / pow((1 + (Discount_Rate / 12)), Period));
                    PVCFSum = PV_of_Cash_Flows + PVCFSum;
                    //printf("%lf\n",ECFSum);
                    fprintf(outFile, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%lf\t%s\t%lf\t%s\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%d\t%d\t%d\t%s\t%lf\t%lf\t%s\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n", Note_Number, Borrower_Name, Acquired_Bank, FDIC_Asset_Pool,
                            Pool, Subpool, Accounting_Treatment, Accrual_Status, Individually_Reviewed, Payment_Type, Coupon_Type, SMM, Valuation_Approach, Coupon, Call_Code,
                            Lifetime_Floor, Discount_Rate, Next_Reset_Coupon, Legal_Balance_Initial, Bank_Balance_Initial, Monthly_CDR_Cohorts,
                            Months_To_Next_Rate_Reset, Months_to_Maturity, Loss_Given_Default, Recovery_Lag, Amortization_Term, Discount_Amortization_Method,
                            Specific_Impairment, Recorded_Investment, Cohort, Period, Legal_Balance, Bank_Balance, Expected_Default,
                            Contractual_Principal, Expected_Principal, Period_Coupon, Contractual_Interest, Expected_Interest, Prepaid_Principal_Contractual,
                            Prepaid_Principal_Expected, Contractual_Ending_Principal,Expected_Ending_Principal, Recovery, Contractual_Cash_Flows, Expected_Cash_Flows,
                            PV_of_Cash_Flows);

                count++;
            }
            fprintf(sumFile, "%s\t%s\t%lf\t%lf\t%lf\n", Note_Number, Call_Code, Months_to_Maturity, ECFSum, PVCFSum);
              }


       fclose(inFile);
    }

    fclose(outFile);
    fclose(sumFile);

    return 0;}


  /**
 * Find maximum between two numbers.
 */
float max(double num1, double num2)
{
    return (num1 > num2 ) ? num1 : num2;
}

/**
 * Find minimum between two numbers.
 */
float min(double num1, double num2)
{
    return (num1 > num2 ) ? num2 : num1;
}
