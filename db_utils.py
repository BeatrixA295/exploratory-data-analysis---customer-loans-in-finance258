#%%
import yaml
#%%
import pandas as pd
#%%
import psycopg2
#%%
from sqlalchemy import create_engine
#%%
import sqlalchemy
#%%
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
loans_df.head(10)
loans_df

print(loans_df.dtypes)
# %%


class DataTransformer:
    def __init__(self, df):
        self.df = df.copy()  # Create a copy of the DataFrame
        
    def transform_data(self):
        self._convert_to_datetime(['issue_date', 'earliest_credit_line'])
        self._extract_numeric_and_convert('employment_length', r'(\d+)')
        self._extract_numeric_and_convert('term', r'(\d+)')
        self._convert_to_categorical(['verification_status', 'grade', 'sub_grade', 'home_ownership', 'loan_status', 'payment_plan', 'purpose', 'application_type'])
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
            


loans_df_transformed = DataTransformer(loans_df)
loans_df_transformed.transform_data()
loans_df_transformed._convert_to_datetime()
loans_df_transformed._extract_numeric_and_convert()
loans_df_transformed._handle_missing_and_convert_to_int
            
            
class DataFrameInfo:
    def __init__(self, df):
        self.df = df.copy()  # Create a copy of the DataFrame
        
    def describe_columns(self):
        return self.df.dtypes
    
    def extract_stats(self):
        return self.df.describe()
    
    def count_distinct_values(self):
        return self.df.select_dtypes(include='category').nunique()
    
    def print_shape(self):
        print("DataFrame shape:", self.df.shape)
        
    def count_null_values(self):
        return self.df.isnull().sum()
    
    # Any other custom methods or EDA tasks can be added here
    
   #%%
class DataTransformer2:
    def __init__(self, df):
     self.df = df.copy()  # Create a copy of the DataFrame
    def reduce_skewness(self, threshold=1):
        numerical_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        skewed_cols = self.df[numerical_cols].apply(lambda x: x.skew()).sort_values(ascending=False)
        skewed_cols = skewed_cols[abs(skewed_cols) > threshold]

        for col in skewed_cols.index:
            if self.df[col].min() > 0:  # Transformation for positive values
                self.df[col] = np.log1p(self.df[col])
            else:
                self.df[col] = np.sign(self.df[col]) * np.log1p(abs(self.df[col]))
                
loans_df_transformed2 = DataTransformer2(loans_df)
loans_df_transformed2.transform_data()
    

