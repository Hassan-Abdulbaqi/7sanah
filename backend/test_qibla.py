import math

def calculate_qibla_direction(latitude, longitude):
    """
    Calculate Qibla direction based on latitude and longitude coordinates
    
    The Qibla direction is calculated using the formula:
    qibla = atan2(sin(lon_k - lon_p), cos(lat_p) * tan(lat_k) - sin(lat_p) * cos(lon_k - lon_p))
    
    Where:
    - lat_k, lon_k are the coordinates of Kaaba (21.4225, 39.8262)
    - lat_p, lon_p are the coordinates of the given point
    """
    # Convert string parameters to float if they are strings
    if isinstance(latitude, str):
        lat_p = float(latitude)
    else:
        lat_p = latitude
        
    if isinstance(longitude, str):
        lon_p = float(longitude)
    else:
        lon_p = longitude
    
    # Coordinates of Kaaba in Mecca
    lat_k = 21.4225  # latitude of Kaaba
    lon_k = 39.8262  # longitude of Kaaba
    
    # Convert to radians
    lat_p_rad = math.radians(lat_p)
    lon_p_rad = math.radians(lon_p)
    lat_k_rad = math.radians(lat_k)
    lon_k_rad = math.radians(lon_k)
    
    # Calculate the Qibla direction
    y = math.sin(lon_k_rad - lon_p_rad)
    x = math.cos(lat_p_rad) * math.tan(lat_k_rad) - math.sin(lat_p_rad) * math.cos(lon_k_rad - lon_p_rad)
    qibla_rad = math.atan2(y, x)
    
    # Convert to degrees and normalize to 0-360
    qibla_deg = math.degrees(qibla_rad)
    qibla_deg = (qibla_deg + 360) % 360
    
    return qibla_deg

# Test with the example coordinates from the API documentation
test_latitude = 19.071017570421
test_longitude = 72.838622286762

qibla_direction = calculate_qibla_direction(test_latitude, test_longitude)
print(f"Qibla direction for coordinates ({test_latitude}, {test_longitude}): {qibla_direction:.6f} degrees")

# Test with a few other locations
test_cases = [
    {"name": "Mecca", "lat": 21.4225, "lon": 39.8262},  # Should be close to 0 (or 360)
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"name": "Cairo", "lat": 30.0444, "lon": 31.2357},
]

for location in test_cases:
    direction = calculate_qibla_direction(location["lat"], location["lon"])
    print(f"Qibla direction for {location['name']} ({location['lat']}, {location['lon']}): {direction:.6f} degrees") 