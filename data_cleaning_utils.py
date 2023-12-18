from db_utils import NullPercentageCalculator

columns = ['id', 'member_id', 'loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc', 'dti', 'delinq_2yrs', 'inq_last_6mths', 'open_accounts', 'total_accounts', 'out_prncp', 'out_prncp_inv', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'last_payment_amount', 'collections_12_mths_ex_med', 'policy_code']
def handle_missing_values(loans_df, drop_threshold=50, impute_threshold_low=0, impute_threshold_high=10, drop_rows_threshold=0.01):

    null_calculator = NullPercentageCalculator(loans_df)
     
    #Count of Null Values 
    null_values = null_calculator.count_null_values()
    print("Initial Null Count:\n", null_values)
             # Calculate and print null percentages
    null_percentages = null_calculator.calculate_null_percentage(columns)
    print("Initial Null Percentages:\n", null_percentages)

    # Drop columns with high null percentages
    null_calculator.drop_high_null_columns(threshold=drop_threshold)
    print("DataFrame after dropping high null columns:\n", null_calculator.df)

    # Impute nulls in columns with moderate amounts of missing values
    null_calculator.impute_nulls(threshold_low=impute_threshold_low, threshold_high=impute_threshold_high)
    print("DataFrame after imputing nulls:\n", null_calculator.df)

    # Drop rows in date columns with high null percentages
    null_calculator.drop_rows_date_columns(threshold=drop_rows_threshold)
    print("DataFrame after dropping rows in date columns:\n", null_calculator.df)

    # Final null counts
    null_count_updated = null_calculator.df.isnull().sum()
    print("Final Null Counts:\n", null_count_updated)