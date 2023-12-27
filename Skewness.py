import matplotlib.pyplot as plt
import seaborn as sns 

def calculate_numerical_skewness(df):
    numerical_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()
    numerical_skewness = df[numerical_columns].skew()
    return numerical_skewness

def plot_numerical_histograms(df):
    numerical_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()

    fig, axes = plt.subplots(nrows=len(numerical_columns), ncols=1, figsize=(8, 4 * len(numerical_columns)))
    for i, column in enumerate(numerical_columns):
        ax = axes[i]
        df[column].hist(ax=ax, bins=30, color='skyblue')
        ax.set_title(f'{column} Histogram')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.grid(axis='y')

    plt.tight_layout()
    plt.show()
    
def log_transform_data(df, column_name):
    df[column_name] = df[column_name].map(lambda i: np.log(i) if i > 0 else 0)
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column_name], kde=True, label="Skewness: %.2f" % (df[column_name].skew()))
    plt.title(f"Log-Transformed Data: {column_name}")
    plt.xlabel("Log(Data Values)")
    plt.legend()
    plt.show()
    
    