import requests

# Define your MISP URL and API key
misp_url = 'https://misp.uni.lu'
api_key = ''

# JSON data for creating the event
json_data = {
    "info": 'dark-pattern-plugin',  # Required
    "distribution": 1,
    "threat_level_id": 1,
    "analysis": 1,
}

headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

try:
    
    # response = requests.get(f"http://misp.uni.lu/tags", headers=headers, verify=True)
    # print(response.json())
    
    # Send POST request to create the event
    response = requests.post(f"{misp_url}/events/add", headers=headers, json=json_data)  # Set verify=False if using self-signed certificate

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        event_id = response.json()['Event']['id']
        print(f'Event created with ID: {event_id}')
        
        # add a tag to the event
        requests.post(f"{misp_url}/events/publish/{event_id}", headers=headers, json={})
        
        # Add object to the event
        data = {
            "Dark pattern strategies": [
                {
                "category": "Dark pattern strategies",
                "value": "127.0.0.1",
                "to_ids": True,
                "disable_correlation": False,
                "distribution": "0",
                "comment": "logged source ip",
                "object_relation": "sensor"
                }
            ]
            }
        response = requests.post(f"{misp_url}/objects/add/{event_id}/12f9392a-9f5e-4251-a13b-cf9eda79ae04", headers=headers, json={})
        
        
        print(response.json())
    else:
        print(f'Failed to create event. Status code: {response.status_code}')
        print(response.text)  # Print the error message from the response, if any

except requests.exceptions.RequestException as e:
    print(f'Error creating event: {e}')
