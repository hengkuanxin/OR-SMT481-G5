
# **SmartBikes: Optimizing Bike-Sharing Systems for Urban Mobility**

## Guide to our Repository:

### Data Preparation:
- **demand_score.ipynb**: to categorise demand levels for each station, outputs station_with_demand.csv
- **distance_matrix.ipynb**: recalculates distances between stations in US metric feet, outputs distance_matrix.csv
- **station_with_demand.csv**: a cleaned dataset of Manhattan trips, with each station classified into a demand level based on binning

### First Stage:
- **bikeprice.ipynb**: to determine the unit value assigned to a bike given a station's trip data and popularity
- **first_stage.py**: used to draft and test the first stage model
- **helpers.py**: helper functions used for data input preparation for the first stage model
- **first_stage_func.py**: actual first stage function used for the final simulation of our model
- This stage was dependent on:
	1. station_with_demand.csv

### Second Stage:
- **avg_ride_count_per_week_weather.csv:** a csv generated from weather_demand.ipynb. It contains the average ride count per week in autumn based off of various weather conditions (normal, sunny, cloudy, rainy)
- **daily_ride_count_by_weather.csv:** a csv generated from weather_demand.ipynb. It contains the average ride count daily in autumn based off of various weather conditions (normal, sunny, cloudy, rainy)
- **weather_demand.ipynb:** a Jupyter notebook that wrangles the 2023 citibike tripdata and 2023 NYC weather data to classify bike trips in Manhattan based off on weather conditions
- **second_stage_v2.ipynb**: used to draft and test the second stage model
- **second_stage_func.py**: actual second stage function used for the final simulation of our model
- This stage was dependent on:
	1. distance_matrix.csv
	2. station_with_demand.csv

### Model Simulation:
- **simulation.ipynb**: full simulation file
This is dependent on:
	1. **first_stage_func.py:** function format for first_stage.py
	2. **second_stage_func.py:** function format for second_stage_v2.ipynb

All other files were used for intermediary steps or drafting to derive values for our analysis.
