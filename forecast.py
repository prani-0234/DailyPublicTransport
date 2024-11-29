import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset
data = pd.read_csv("E:\Daily_Public_Transport_Passenger_Journeys_by_Service_Type_20241129.csv")

# Display the first few rows of the dataset
print(data.head())

# Clean and prepare the data
for column in ['Local Route', 'Light Rail', 'Peak Service', 'Rapid Route', 'School']:
    data[column] = data[column].replace({'\"': '', ',': ''}, regex=True).replace('', pd.NA)
    data[column] = data[column].fillna(0).astype(int)

# Convert 'Date' to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

# Set Date as index and set frequency
data.set_index('Date', inplace=True)
data = data.asfreq('D')  # Set frequency to daily

# Forecasting function using ARIMA
def forecast_service(service_name):
    # Fit ARIMA model
    model = ARIMA(data[service_name], order=(5, 1, 0))  # You can adjust the order based on your needs
    model_fit = model.fit()

    # Forecast for the next 7 days
    forecast = model_fit.forecast(steps=7)
    
    # Create a date range for the forecasted dates
    last_date = data.index[-1]
    forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7, freq='D')
    
    # Plot the results
    plt.figure(figsize=(10, 5))
    plt.plot(data[service_name], label='Historical Data')
    plt.plot(forecast_index, forecast, label='Forecast', color='red')
    plt.title(f'Forecast for {service_name} for Next 7 Days')
    plt.xlabel('Date')
    plt.ylabel('Number of Passengers')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.legend()
    plt.show()


    return forecast

# Forecasting for each service type
local_route_forecast = forecast_service('Local Route')
light_rail_forecast = forecast_service('Light Rail')
peak_service_forecast = forecast_service('Peak Service')
rapid_route_forecast = forecast_service('Rapid Route')
school_forecast = forecast_service('School')

# Displaying forecasts
print("Local Route Forecast:")
print(local_route_forecast)

print("\nLight Rail Forecast:")
print(light_rail_forecast)

print("\nPeak Service Forecast:")
print(peak_service_forecast)

print("\nRapid Route Forecast:")
print(rapid_route_forecast)

print("\nSchool Forecast:")
print(school_forecast)