import json
import requests
 
json_object = ''
# Opening JSON file
with open('JSON/query/getMarketData.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)



response = requests.post('https://stockx.com/api/p/e', cookies=json_object['cookies'], headers=json_object['headers'], json=json_object['data']).json()

with open('response/response.json', 'w') as file:
    json.dump(response, file)
