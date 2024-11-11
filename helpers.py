import csv

# Returns dictionary of Manhattan stations: 
#   station_id: {station_name, capacity, lng, lat}
def get_manhattan_stations():
    """Return the list of Manhattan stations from the manhattan_stations.csv file."""
    stations_dict = {}

    with open("datasets/station_with_demand.csv", "r") as f:
        csv_data = csv.reader(f)
        next(csv_data) # Skips the header row

        for row in csv_data:
            stations_dict[row[0]] = {
                'station_name': row[1],
                'capacity': int(row[2]),
                'lng': float(row[3]),
                'lat': float(row[4]),
                'demand_level': row[8]
            }

    return stations_dict

def add_benefit_score(stations_dict):
    benefit_values = {
        'Lowest': 5.965713516563833,
        'Low': 5.8684194073530325,
        'Medium': 5.816980433485934,
        'Highest': 5.79309663001927
    }

    for k in stations_dict:
        stations_dict[k]['benefit_value'] = benefit_values[stations_dict[k]['demand_level']] 

    return stations_dict

