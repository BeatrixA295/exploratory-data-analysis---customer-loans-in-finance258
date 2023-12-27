import yaml 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import seaborn as sns
import missingno as msno 
import matplotlib.pyplot as plt
with open('credentials.yaml', 'r') as f:
    credentials = yaml.safe_load(f)
#%%
class RDSDatabaseConnector:
    def __init__(df, credentials):
        df.credentials = credentials

    #PROBLEM WITH STRING LITERAL EU-WEST1 AND INDENTATION IN NEXT CODE
    def _create_engine(df):
        engine = create_engine(f"postgresql+psycopg2://{df.credentials['RDS_USER']}:{df.credentials['RDS_PASSWORD']}@{df.credentials['RDS_HOST']}:{df.credentials['RDS_PORT']}/{df.credentials['RDS_DATABASE']}")
        return engine
    
    def initialise_engine(df):
        df.engine = df._create_engine()

    def data_extraction(df, table_name='loan_payments'):
        query = f"SELECT * FROM loan_payments;"
        data = pd.read_sql(query, df.engine)
        return data
    
    def save_to_file(df, data, file_path='loan_payments_data.csv'):
        data.to_csv(file_path, index=False)

    def load_loan_data(df, file_path='loan_payments_data.csv'):
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

df = pd.read_csv('loan_payments_data.csv')
#%%

class DataFrameTransform:
       
        
    def _convert_to_datetime(df, date_columns):
        for col in date_columns:
            try:
                # convert using the standard date format
                df[col] = pd.to_datetime(df[col])
            except ValueError:
                try: 
                    # convert using a specific format if standard conversion fails
                    df[col] = pd.to_datetime(df[col], format='%Y-%m')
                except ValueError:
                    # If specific format also fails, print error
                    print(f"Column {col} cannot be converted to datetime")

            
    def drop_rows_date_columns(df):
        date_columns = ['issue_date', 'earliest_credit_line', 'last_payment_date', 'last_credit_pull_date']
        df_copy = df.drop(date_columns, axis=1).copy()
        return df_copy

            
    def _extract_numeric_and_convert(df, column, pattern):
        df[column] = df[column].str.extract(pattern).astype(float)
        
    def _convert_to_categorical(df, columns):
        for col in columns:
            df[col] = df[col].astype('category')
            
    def _handle_missing_and_convert_to_int(df, columns):
        for col in columns:
            df[col] = df[col].fillna(0).astype(int) 
            
    def reduce_skewness(df, threshold=1):
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        skewed_cols = df[numerical_cols].apply(lambda x: x.skew()).sort_values(ascending=False)
        skewed_cols = skewed_cols[abs(skewed_cols) > threshold]

        for col in skewed_cols.index:
            if df[col].min() > 0:  # Transformation for positive values
                df[col] = np.log1p(df[col])
            else:
                df[col] = np.sign(df[col]) * np.log1p(abs(df[col]))
   
    def convert_to_object(df, column_name):
        df[column_name] = df[column_name].astype('object')
    
    def convert_to_float(df, column_name):
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(float)
        return df

    def convert_to_int(df, column_name):
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype(int)
        return df

    def convert_to_category(df, column_name):
        df[column_name] = df[column_name].astype('category')

                
#%% 
class NullPercentageCalculator:
        def list_columns(df):
            columns_list = list(df.columns)
            return columns_list        

        def count_null_values(df):
            return df.isnull().sum()

        def calculate_null_percentage(df, columns):
            columns = df.columns 
            percent_missing = df[columns].isnull().sum() * 100 / len(df)
            return percent_missing

        def drop_high_null_columns(df, threshold=50):
            percent_missing = df.isnull().sum() * 100 / len(df)
            columns_to_drop = percent_missing[percent_missing > threshold].index.tolist()
            df.drop(columns = columns_to_drop, inplace=True)
            return df, columns_to_drop

        def impute_nulls(df, threshold_low=0, threshold_high=10):
            percent_missing = df.isnull().sum() * 100 / len(df)
            columns_to_impute = percent_missing[(percent_missing > threshold_low) & (percent_missing < threshold_high)].index.tolist()

            for col in columns_to_impute:
                if df[col].dtype == 'object':
                    df[col].fillna(df[col].mode()[0], inplace=True)
                else:
                    if abs(df[col].skew()) > 1:
                        df[col].fillna(df[col].median(), inplace=True)
                    else:
                        df[col].fillna(df[col].mean(), inplace=True)
            return df 
                        
        def drop_rows_date_columns(df, threshold=0.01):
            date_columns = ['issue_date', 'earliest_credit_line', 'last_payment_date', "last_credit_pull_date"]
            for col in date_columns:
                if col in df.columns:
                    null_percentage = df[col].isnull().mean()
                    if null_percentage > threshold:
                        df.dropna(subset=[col], inplace=True)
            return df 


#%%
            
class DataFrameInfo:
        
        print("\nStatistical Values:")
        print(df.describe)
        print ('Column_Types: ')
        column_types = df.dtypes
        print(column_types)
        print('Number of Distinct Values: ')
        distinct_values = {}
        for col in df.columns:
            distinct_values[col] = df[col].nunique()
        print((distinct_values))
        print('DataFrame Shape')
        print(df.shape)

    
    # Any other custom methods or EDA tasks can be added here
    #%%

# Add more functions as needed for additional data types...

        
#%%
class Plotter:                         

    def show_matrix_before(df):
        msno.matrix(df)
        plt.title('Missing Values Matrix Before Handling')
        plt.show()

    def show_heatmap_before(df):
        msno.heatmap()
        plt.title('Missing Values Heatmap Before Handling')
        plt.show()

    def show_matrix_after(df):
            msno.matrix(df)
            plt.title('Missing Values Matrix After Handling')
            plt.show()

    def show_heatmap_after(df):
        msno.heatmap(df)
        plt.title('Missing Values Heatmap After Handling')
        plt.show()

    
    def histogram(df, column, bins):
        plt.hist(df[column], bins=bins)
        plt.tight_layout()
        plt.show()

# %%
