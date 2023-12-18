import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sqlalchemy
import seaborn as sns
import missingno as msno 
import matplotlib.pyplot as plt
with open('credentials.yaml', 'r') as f:
    credentials = yaml.safe_load(f)
#%%
class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials

    #PROBLEM WITH STRING LITERAL EU-WEST1 AND INDENTATION IN NEXT CODE
    def _create_engine(self):
        engine = create_engine(f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}")
        return engine
    
    def initialise_engine(self):
        self.engine = self._create_engine()

    def data_extraction(self, table_name='loan_payments'):
        query = f"SELECT * FROM loan_payments;"
        data = pd.read_sql(query, self.engine)
        return data
    
    def save_to_file(self, data, file_path='loan_payments_data.csv'):
        data.to_csv(file_path, index=False)

    def load_loan_data(self, file_path='loan_payments_data.csv'):
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
#%%
loan_data = RDSDatabaseConnector(credentials)
loan_data._create_engine()
loan_data.initialise_engine()
loan_data.data_extraction()
loan_data.data_extraction('loan_payments')
loan_data.save_to_file(data=loan_data.data_extraction('loan_payments'), file_path='loan_payments_data.csv')
loaded_data = loan_data.load_loan_data('loan_payments_data.csv')
print(loaded_data) 

loans_df = pd.read_csv('loan_payments_data.csv')
#%%

class DataFrameTransform:
    def __init__(self, df):
        self.df = df.copy()  # Create a copy of the DataFrame
        
    def transform_data(self):
        skewed_columns = ['id', 'member_id', 'loan_amount', 'funded_amount_inv', 'annual_inc', 'delinq_2yrs', 'inq_last_6mths','mths_since_last_delinq', 'mths_since_last_record','open_accounts', 'total_accounts','collections_12_ex_med','mths_since','last_major_derog','policy_code', 'int_rate', 'instalment','dti', 'out_prncp', 'total_payment_inv,total_rec_prncp','total_rec_int','total_rec_late_fees','recoveries','collection_recovery_fee' ,'last_payment_amount']
        date_columns =  ['issue_date', 'earliest_credit_line','last_payment_date',"last_credit_pull_date"]
        self._convert_to_datetime(date_columns)
        self._extract_numeric_and_convert('employment_length', r'(\d+)')
        self._extract_numeric_and_convert('term', r'(\d+)')
        self._convert_to_categorical(['grade', 'sub_grade', 'loan_status', 'payment_plan', 'purpose', 'application_type'])
        self._handle_missing_and_convert_to_int(['mths_since_last_delinq', 'mths_since_last_record', 'mths_since_last_major_derog'])
        
    def _convert_to_datetime(self, columns):
        for col in columns:
            self.df[col] = pd.to_datetime(self.df[col], format='%b-%Y', errors='coerce')
            
    def _extract_numeric_and_convert(self, column, pattern):
        self.df[column] = self.df[column].str.extract(pattern).astype(float)
        
    def _convert_to_categorical(self, columns):
        for col in columns:
            self.df[col] = self.df[col].astype('category')
            
    def _handle_missing_and_convert_to_int(self, columns):
        for col in columns:
            self.df[col] = self.df[col].fillna(0).astype(int) 
            
    def reduce_skewness(self, threshold=1):
        numerical_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        skewed_cols = self.df[numerical_cols].apply(lambda x: x.skew()).sort_values(ascending=False)
        skewed_cols = skewed_cols[abs(skewed_cols) > threshold]

        for col in skewed_cols.index:
            if self.df[col].min() > 0:  # Transformation for positive values
                self.df[col] = np.log1p(self.df[col])
            else:
                self.df[col] = np.sign(self.df[col]) * np.log1p(abs(self.df[col]))
                
#%% 
class NullPercentageCalculator:
        def __init__(self, df):
            self.df = df
                            
        def count_null_values(self):
            return self.df.isnull().sum()

        def calculate_null_percentage(self,column):
            percent_missing = self.df[column].isnull().sum() * 100 / len(self.df)
            return percent_missing

        def drop_high_null_columns(self, threshold=50):
            percent_missing = self.df.isnull().sum() * 100 / len(self.df)
            columns_to_drop = percent_missing[percent_missing > threshold].index.tolist()
            self.df.drop(columns=columns_to_drop, inplace=True)

        def impute_nulls(self, threshold_low=0, threshold_high=10):
            percent_missing = self.df.isnull().sum() * 100 / len(self.df)
            columns_to_impute = percent_missing[(percent_missing > threshold_low) & (percent_missing < threshold_high)].index.tolist()

            for col in columns_to_impute:
                if self.df[col].dtype == 'object':
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                else:
                    if abs(self.df[col].skew()) > 1:
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        self.df[col].fillna(self.df[col].mean(), inplace=True)

        def drop_rows_date_columns(self, threshold=0.01):
            date_columns = ['issue_date', 'earliest_credit_line', 'last_payment_date', "last_credit_pull_date"]
            for col in date_columns:
                if col in self.df.columns:
                    null_percentage = self.df[col].isnull().mean()
                    if null_percentage > threshold:
                        self.df.dropna(subset=[col], inplace=True)

#%%
            
class DataFrameInfo:
        def __init__(self, df):
            self.df = df.copy()  # Create a copy of the DataFrame
            
        def describe_columns(self):
            return self.df.dtypes
        
        def extract_stats(self):
            return self.df.describe()
        
        def count_distinct_values(self):
            return self.df.select_dtypes.nunique()
        
        def print_shape(self):
            print("DataFrame shape:")
            return self.df.shape

    
    # Any other custom methods or EDA tasks can be added here
#%%
class Plotter:
                def __init__(self, df):
                    self.df = df
                                                        
                def show_matrix_before(self):
                    msno.matrix(self.df)
                    plt.title('Missing Values Matrix Before Handling')
                    plt.show()

                def show_heatmap_before(self):
                    msno.heatmap(self.df)
                    plt.title('Missing Values Heatmap Before Handling')
                    plt.show()

                def show_matrix_after(self):
                        msno.matrix(self.df)
                        plt.title('Missing Values Matrix After Handling')
                        plt.show()

                def show_heatmap_after(self):
                    msno.heatmap(self.df)
                    plt.title('Missing Values Heatmap After Handling')
                    plt.show()

                
                def plot_skew(loans_df, threshold=1):
                    plt.figure(figsize=(14, 8))  # Adjust the figure size as needed
                    skewed_columns = [['id', 'member_id', 'loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc', 'dti', 'delinq_2yrs', 'inq_last_6mths', 'mths_since_last_delinq', 'mths_since_last_record', 'open_accounts', 'total_accounts', 'out_prncp', 'out_prncp_inv', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee', 'recoveries', 'collection_recovery_fee', 'last_payment_amount', 'collections_12_mths_ex_med', 'mths_since_last_major_derog', 'policy_code']]  # Your list of columns
                    
                    num_columns = len(skewed_columns)
                    
                    for idx, col in enumerate(skewed_columns, start=1):
                        plt.subplot(1, num_columns, idx)
                        sns.histplot(loans_df[col], kde=True, bins=3000, alpha=0.5)
                        plt.xlabel("Value")
                        plt.ylabel("Frequency")
                        plt.title(f'Skewed Column: {col}')
                
                plt.suptitle('Histograms of Skewed Columns', y=1.05)  # Title for the entire plot
                plt.tight_layout()
                plt.show()


# %%
