import urllib.request
from bs4 import BeautifulSoup

# Input data
url = input("Enter URL: ")  # Enter the starting URL
count = int(input("Enter count: "))  # Number of repetitions
position = int(input("Enter position: ")) - 1  # Link position (starting from 1, so subtract 1)

# Main process
print("Retrieving:", url)
for i in range(count):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    # Find all <a> tags
    tags = soup.find_all("a")
    if len(tags) < position:
        print("Not enough links on the page!")
        break

    # Get the URL at the specified position
    url = tags[position].get("href")
    print("Retrieving:", url)

# Last URL
print("Last URL retrieved:", url)
