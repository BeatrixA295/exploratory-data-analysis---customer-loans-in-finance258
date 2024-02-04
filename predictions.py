import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
def summarize_recovery(df):
    # Assuming 'recoveries' represent recovered amount and 'funded_amount' is the total funded amount
    total_funded = df['funded_amount_inv'].sum()
    total_recovered = df['total_payment'].sum()
    
    # Calculate percentage of loans recovered
    percentage_recovered = (total_recovered / total_funded) * 100
    
    # Visualize the results
    plt.rcParams.update({'font.size': 14})
    labels = ['Recovered', 'Remaining']
    sizes = [percentage_recovered, 100 - percentage_recovered]
    colours = ['#19FF19', '#E3242B']
    plt.pie(sizes, labels=labels, colors= colours, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  
    plt.title('Percentage of Loans Recovered')
    plt.show()
    return percentage_recovered

def calculate_historical_charged_off(df):
    # Count Charged Off Loans
    charged_off_loans = len(df[df['loan_status'] == 'Charged Off'])

    # Total Payments for Charged Off Loans
    total_payment_charged_off = df.loc[df['loan_status'] == 'Charged Off', 'total_payment'].sum()

    # Calculate Historical Percentage
    percentage_charged_off = (charged_off_loans / len(df)) * 100

    # Display the Results
    print("Total amount of Charged Off Loans:", charged_off_loans)
    print("Total Amount paid unti Charged Off occured:", total_payment_charged_off)
    print("Historical Percentage of Charged Off Loans:", percentage_charged_off)
    print(round(percentage_charged_off,2), '%')
    


def calculate_projected_loss(df):
    # Filter loans marked as 'Charged Off'
    charged_off_loans = df[df['loan_status'] == 'Charged Off'].copy()

    # Extract numeric part from 'term' column and convert it to integer
    charged_off_loans['term_numeric'] = charged_off_loans['term'].str.extract('(\d+)').astype(int)

    # Calculate outstanding principal for Charged Off loans
    outstanding_principal = charged_off_loans['out_prncp'].sum()

    # Assuming 'int_rate' column represents interest rates and 'term' represents remaining term in months
    # Calculate remaining interest payments for Charged Off loans
    remaining_interest = (charged_off_loans['int_rate'] / 100) * outstanding_principal * charged_off_loans['term_numeric']

    # Calculate projected loss considering outstanding principal and remaining interest
    projected_loss = outstanding_principal + remaining_interest

    plt.figure(figsize=(8, 6))
    plt.plot(charged_off_loans['term_numeric'], remaining_interest, marker='o', linestyle='-', color='red')
    plt.title('Projected Loss Over Remaining Term for Charged Off Loans')
    plt.xlabel('Remaining Term')
    plt.ylabel('Projected Loss')
    plt.grid(True)
    plt.show()


def plot_possible_indicators(df):
    grouped_data = df.groupby(['purpose', 'loan_status']).size().unstack(fill_value=0)
    fig, ax = plt.subplots()

    # Bar width can be adjusted as needed
    bar_width = 0.2

    # Position of bars on x-axis
    bar_positions = np.arange(len(grouped_data.index))

    # Offset each bar within a group
    offset = np.linspace(-0.35, 0.35, len(grouped_data.columns))

    for i, status in enumerate(grouped_data.columns):
        ax.bar(
            bar_positions + offset[i],
            grouped_data[status],
            width=bar_width,
            label=status
        )

    # Set labels and title
    ax.set_xlabel('Purpose')
    ax.set_ylabel('Count')
    ax.set_title('Loan Status by Purpose')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(grouped_data.index)
    ax.legend()

    # Show the plot
    plt.show()





