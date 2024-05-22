import requests
import pandas as pd

def get_place_details(api_key, query, location):
    # Base URL for the Places API
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Parameters for the API request
    params = {
        'query': f"{query} in {location}",
        'key': api_key
    }

    # Make the request
    response = requests.get(base_url, params=params)
    results = response.json().get('results', [])

    # List to store business details
    business_details = []

    for result in results:
        name = result.get('name')
        address = result.get('formatted_address')
        place_id = result.get('place_id')

        # Get more details for each place using the place_id
        place_details = get_place_detail(api_key, place_id)

        phone = place_details.get('formatted_phone_number', '')
        website = place_details.get('website', '')
        email = ''  # Email is not provided by the Places API

        business_details.append([name, phone, website, email, address])

    # Create a DataFrame and export to Excel
    df = pd.DataFrame(business_details, columns=['Name', 'Phone', 'Website', 'Email', 'Address'])
    df.to_excel('business_details.xlsx', index=False)

    print(f"Fetched {len(business_details)} businesses and saved to business_details.xlsx")

def get_place_detail(api_key, place_id):
    # Base URL for the Place Details API
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    # Parameters for the API request
    params = {
        'place_id': place_id,
        'key': api_key,
        'fields': 'formatted_phone_number,website'
    }

    # Make the request
    response = requests.get(base_url, params=params)
    result = response.json().get('result', {})
    return result

if __name__ == "__main__":
    api_key = input("Enter your Google Places API key: ")
    query = input("Enter the type of business: ")
    location = input("Enter the city or postal code: ")
    get_place_details(api_key, query, location)






