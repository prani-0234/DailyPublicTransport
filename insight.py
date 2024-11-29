import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv("E:\Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20241129.csv")

# Display the first few rows of the dataset
print(data.head())

# Data Cleaning
# Remove commas from numeric columns and convert them to integers
for column in ['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School', 'Other']:
    # Remove commas and quotes, replace empty strings with NaN, then fill NaN with 0
    data[column] = data[column].replace({'\"': '', ',': ''}, regex=True).replace('', pd.NA)
    
    # Fill NaN values with 0
    data[column] = data[column].fillna(0)

    # Convert to integer
    data[column] = data[column].astype(int)

# Convert 'Date' to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

# Exploratory Data Analysis (EDA)
# Descriptive statistics
print(data.describe())

# Set Date as index
data.set_index('Date', inplace=True)

# Plotting
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']  # Custom color palette

data[['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School', 'Other']].plot(color=colors)

plt.title('Passenger Journeys by Service Type Over Time', fontsize=16)
plt.ylabel('Number of Passengers', fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)  # Add grid lines for easier reading

# Adding a legend with a larger font size
plt.legend(title='Service Type', fontsize=12, loc='upper left')

# Adjust layout to prevent clipping of tick-labels
plt.tight_layout()
plt.show()

# Seasonal Trends: Monthly average passenger journeys
# Aggregate data by month using resample
monthly_data = data.resample('ME').mean()  # Calculate monthly averages

# Plotting
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']  # Custom color palette

monthly_data[['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School', 'Other']].plot(color=colors)

plt.title('Monthly Average Passenger Journeys by Service Type', fontsize=16)
plt.ylabel('Average Passengers', fontsize=14)
plt.xlabel('Month', fontsize=14)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)  # Add grid lines for easier reading
plt.legend(title='Service Type', fontsize=12)
plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
plt.show()

# Correlation Analysis
correlation_matrix = data[['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School', 'Other']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Between Service Types')
plt.show()

# Insights Generation
total_passengers = data[['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School', 'Other']].sum()
print("Total Passengers by Service Type:")
print(total_passengers)

# Calculate and print max and min total passengers for each service type
max_passengers = total_passengers.max()
min_passengers = total_passengers.min()

print("\nMaximum Total Passengers by Service Type:")
print(total_passengers[total_passengers == max_passengers])

print("\nMinimum Total Passengers by Service Type:")
print(total_passengers[total_passengers == min_passengers])

# Identify peak service usage
peak_service_usage = data['Peak Service'].groupby(data.index.month).sum()
print("Monthly Peak Service Usage:")
print(peak_service_usage)

# Identify the month with the highest overall passenger journeys for Local Route
highest_month = data['Local Route'].groupby(data.index.month).sum().idxmax()
print(f"Month with highest local route journeys: {highest_month}")
'''
# Save cleaned data for further analysis if needed
data.to_csv('cleaned_public_transport_data.csv', index=False)
'''