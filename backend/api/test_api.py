import requests
import json

def test_api():
    base_url = 'http://localhost:8000/api'
    
    # Test hijri-months endpoint
    print("Testing hijri-months endpoint...")
    response = requests.get(f'{base_url}/hijri-months/')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {data['count']} Hijri months")
        print(f"First month: {data['results'][0]['name_en']} ({data['results'][0]['name_ar']})")
        month_id = data['results'][0]['id']
    else:
        print(f"Error: {response.status_code}")
        return
    
    # Test hijri-months detail endpoint
    print("\nTesting hijri-months detail endpoint...")
    response = requests.get(f'{base_url}/hijri-months/{month_id}/')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Month details: {data['name_en']} ({data['name_ar']})")
        print(f"Events count: {len(data['events'])}")
        print(f"Astronomical events count: {len(data['astronomical_events'])}")
    else:
        print(f"Error: {response.status_code}")
    
    # Test hijri-months/current/ endpoint
    print("\nTesting hijri-months/current/ endpoint...")
    response = requests.get(f'{base_url}/hijri-months/current/')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Current month: {data['name_en']} ({data['name_ar']})")
    else:
        print(f"Error: {response.status_code}")
    
    # Test hijri-events endpoint
    print("\nTesting hijri-events endpoint...")
    response = requests.get(f'{base_url}/hijri-events/')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} Hijri events")
        if len(data) > 0:
            print(f"First event: {data[0]['title_en']} ({data[0]['title_ar']})")
    else:
        print(f"Error: {response.status_code}")
    
    # Test hijri-events/by_month/ endpoint
    print("\nTesting hijri-events/by_month/ endpoint...")
    response = requests.get(f'{base_url}/hijri-events/by_month/?month_id={month_id}')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} events for the month")
        if len(data) > 0:
            print(f"First event: {data[0]['title_en']} ({data[0]['title_ar']})")
    else:
        print(f"Error: {response.status_code}")
    
    # Test astronomical-events endpoint
    print("\nTesting astronomical-events endpoint...")
    response = requests.get(f'{base_url}/astronomical-events/')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} astronomical events")
        if len(data) > 0:
            print(f"First event: {data[0]['title_en']} ({data[0]['title_ar']})")
    else:
        print(f"Error: {response.status_code}")
    
    # Test astronomical-events/by_month/ endpoint
    print("\nTesting astronomical-events/by_month/ endpoint...")
    response = requests.get(f'{base_url}/astronomical-events/by_month/?month_id={month_id}')
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data)} astronomical events for the month")
        if len(data) > 0:
            print(f"First event: {data[0]['title_en']} ({data[0]['title_ar']})")
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    test_api() 