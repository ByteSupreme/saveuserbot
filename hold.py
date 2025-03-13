import requests
import time

url = "https://severe-nolie-rajujaago-6ab8644a.koyeb.app/"

while True:
    try:
        response = requests.get(url)
        print("Status Code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    
    time.sleep(20)  # Wait for 20 seconds before the next request
