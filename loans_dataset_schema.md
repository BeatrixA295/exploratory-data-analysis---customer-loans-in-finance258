`# Full loans dataset schema

- **id**: unique id of the loan category int
- **member_id**: id of the member to took out the loan int
- **loan_amount**: amount of loan the applicant received float 
- **funded_amount**: The total amount committed to the loan at the point in time  float
- **funded_amount_inv**: The total amount committed by investors for that loan at that point in time
- **term**: The number of monthly payments for the loan categorical 
- **int_rate**: Interest rate on the loan float 
- **instalment**: The monthly payment owned by the borrower
- **grade**: LC assigned loan grade categorical 
- **sub_grade**: LC assigned loan sub grade categorical 
- **employment_length**: Employment length in years. categorical
- **home_ownership**: The home ownership status provided by the borrower categorical 
- **annual_inc**: The annual income of the borrower float 
- **verification_status**: Indicates whether the borrowers income was verified by the LC or the income source was verified categorical 
- **issue_date:** Issue date of the loan datetime 
- **loan_status**: Current status of the loan categorical 
- **payment_plan**: Indicates if a payment plan is in place for the loan. Indication borrower is struggling to pay.
- **purpose**: A category provided by the borrower for the loan request.
- **dti**: A ratio calculated using the borrowerâ€™s total monthly debt payments on the total debt obligations, excluding mortgage and the requested LC loan, divided by the borrowerâ€™s self-reported monthly income.
- **delinq_2yr**: The number of 30+ days past-due payment in the borrower's credit file for the past 2 years.
- **earliest_credit_line**: The month the borrower's earliest reported credit line was opened
- **inq_last_6mths**: The number of inquiries in past 6 months (excluding auto and mortgage inquiries)
- **mths_since_last_record**: The number of months since the last public record.
- **open_accounts**: The number of open credit lines in the borrower's credit file.
- **total_accounts**: The total number of credit lines currently in the borrower's credit file
- **out_prncp**: Remaining outstanding principal for total amount funded
- **out_prncp_inv**: Remaining outstanding principal for portion of total amount funded by investors
- **total_payment**: Payments received to date for total amount funded
- **total_rec_int**: Interest received to date
- **total_rec_late_fee**: Late fees received to date
- **recoveries**: post charge off gross recovery
- **collection_recovery_fee**: post charge off collection fee
- **last_payment_date**: Last month payment was received
- **last_payment_amount**: Last total payment amount received
- **next_payment_date**: Next scheduled payment date
- **last_credit_pull_date**: The most recent month LC pulled credit for this loan
- **collections_12_mths_ex_med**: Number of collections in 12 months excluding medical collections
- **mths_since_last_major_derog**: Months since most recent 90-day or worse rating
- **policy_code**: publicly available policy_code=1 new products not publicly available policy_code=2
- **application_type**: Indicates whether the loan is an individual application or a joint application with two co-borrowers


- **Float**
float_columns = ['loan_amount','funded_amount','funded_amount_inv','int_rate','instalment','annual_inc','dti','out_prncp','out_prncp_inv','total_payment','total_payment_inv','total_rec_prncp','total_rec_int','total_rec_late_fee','recoveries','collection_recovery_fee','last_payment_amount']

- **Category**
['term','grade','sub_grade','employment_length']


- **Integer**
integer_columns = ['delinq_2yrs','inq_last_6mths','open_accounts','total_accounts','inq_last_6mths','collections_12_mths_ex_med','policy_code']


- **Object**
object_columns = ['home_ownership','verification_status','loan_status','payment_plan','purpose','application_type']

- **Date**
['issue_date','earliest_credit_line','last_payment_date','last_credit_pull_date']



- **Removed**
mths_since_last_delinq, 'mths_since_last_record', 'next_payment_date', 'mths_since_last_major_derog'