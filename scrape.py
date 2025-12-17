import re
import requests
from bs4 import BeautifulSoup
import pickle

# URL of the website to scrape
url = "https://www.remotecentral.com/cgi-bin/codes/broksonic/ctgv-4563tct/"  # Replace with the target URL

# Send GET request
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Regex pattern for span ids like HexCode123
pattern = re.compile(r"HexCode\d+")

# Dictionary to store results
hex_dict = {}

# Loop through all spans matching the pattern
for span in soup.find_all("span", id=pattern):
    tr = span.find_parent("tr")  # Find the parent <tr>
    if not tr:
        continue
    
    td = tr.find("td", class_="filematchleft")  # Find <td class="filematchleft">
    if not td:
        continue
    
    b_tag = td.find("b")  # Find the <b> element inside <td>
    if not b_tag:
        continue
    
    key = b_tag.get_text(strip=True)
    value = span.get_text(strip=True).split(' ')
    
    hex_dict[key] = value

# URL of the website to scrape
url = "https://www.remotecentral.com/cgi-bin/codes/broksonic/ctgv-4563tct/page-2/"  # Replace with the target URL

# Send GET request
response = requests.get(url)
if response.status_code != 200:
    raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Regex pattern for span ids like HexCode123
pattern = re.compile(r"HexCode\d+")

# Loop through all spans matching the pattern
for span in soup.find_all("span", id=pattern):
    tr = span.find_parent("tr")  # Find the parent <tr>
    if not tr:
        continue
    
    td = tr.find("td", class_="filematchleft")  # Find <td class="filematchleft">
    if not td:
        continue
    
    b_tag = td.find("b")  # Find the <b> element inside <td>
    if not b_tag:
        continue
    
    key = b_tag.get_text(strip=True)
    value = span.get_text(strip=True).split(' ')
    
    hex_dict[key] = value


# Print the dictionary
with open('codes.pkl','wb') as file:
    pickle.dump(hex_dict,file)
