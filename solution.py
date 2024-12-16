import urllib.request
import urllib.parse
import json

# Base URL for the API
api_url = "http://py4e-data.dr-chuck.net/opengeo?"

# Input location
location = input("Enter location: ")
params = {"q": location}
url = api_url + urllib.parse.urlencode(params)

# Retrieve JSON data from the API
print("Retrieving", url)
response = urllib.request.urlopen(url)
data = response.read().decode()
print("Retrieved", len(data), "characters")

# Parse JSON data
json_data = json.loads(data)

# Attempt to extract "plus_code" from JSON
try:
    plus_code = json_data["features"][0]["properties"]["plus_code"]
    print("Plus code:", plus_code)
except (KeyError, IndexError):
    print("No plus code found.")
