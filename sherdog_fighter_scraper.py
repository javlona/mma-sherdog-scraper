import requests
import json
import validators
from bs4 import BeautifulSoup


def is_valid_url(url):
    """ Check if the given URL is valid. """
    return validators.url(url)

def get_fighter_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Mimicking a web browser

    try:
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code != 200:
            return {'Error': f'HTTP request failed with status code {response.status_code}'}

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract detailed data with error handling for missing data
        fighter_data = {
            'Name': soup.find('span', class_='fn').get_text(strip=True) if soup.find('span', class_='fn') else 'N/A',
            'Nationality': soup.find('strong', text='Nationality:').find_next_sibling().get_text(strip=True) if soup.find('strong', text='Nationality:') else 'N/A',
            'Age': soup.find('span', class_='item birthday').get_text(strip=True) if soup.find('span', class_='item birthday') else 'N/A',
            'Height': soup.find('strong', text='Height:').find_next_sibling().get_text(strip=True) if soup.find('strong', text='Height:') else 'N/A',
            'Weight': soup.find('strong', text='Weight:').find_next_sibling().get_text(strip=True) if soup.find('strong', text='Weight:') else 'N/A',
            'Association': soup.find('strong', text='Association:').find_next_sibling().get_text(strip=True) if soup.find('strong', text='Association:') else 'N/A',
            'Weight Class': soup.find('strong', text='Weight Class:').find_next_sibling().get_text(strip=True) if soup.find('strong', text='Weight Class:') else 'N/A',
            'Wins': soup.find('span', class_='counter').get_text(strip=True) if soup.find('span', class_='counter') else 'N/A',  # Assuming 'Wins' are in 'span' with class 'counter'
            'Losses': soup.find('span', class_='graph_tag').get_text(strip=True) if soup.find('span', class_='graph_tag') else 'N/A',  # Assuming 'Losses' are in 'span' with class 'graph_tag'
            # Add similar lines for other fields...
        }

        return fighter_data

    except requests.RequestException as e:
        return {'Error': str(e)}

def save_fighter_data(fighter_info, filename='fighter_data.json'):
    try:
        # Load existing data or initialize an empty list
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        # Check if the fighter is already in the data
        existing_entry = next((item for item in data if item['Name'] == fighter_info['Name']), None)
        if existing_entry:
            print(f"Fighter {fighter_info['Name']} already exists in the file.")
        else:
            # Append new fighter data
            data.append(fighter_info)

            # Save updated data
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Fighter {fighter_info['Name']} added to the file.")

    except Exception as e:
        print(f"Error saving data: {e}")

# Example usage
# url = 'https://www.sherdog.com/fighter/Example-Fighter-12345'
# fighter_info = get_fighter_info(url)

def main():
    input_url = input("Enter the URL of the fighter's profile on Sherdog: ")

    if is_valid_url(input_url):
        fighter_info = get_fighter_info(input_url)

        if 'Error' in fighter_info:
            print(fighter_info['Error'])
        else:
            save_fighter_data(fighter_info)
    else:
        print("The URL is invalid. Please enter a valid URL.")

if __name__ == '__main__':
    main()


# Handle error in fighter_info before saving
# if 'Error' in fighter_info:
#     print(fighter_info['Error'])
# else:
#     save_fighter_data(fighter_info)