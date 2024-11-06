import requests
import api_keys

response = requests.get("https://yesno.wtf/api")
print(response.json())

nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={api_keys.nasa_api_key}"

response = requests.get(nasa_url)
print(response.json())
