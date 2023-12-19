import requests
import json

def getRetailPrice_ReleaseDate(productName):
    url = 'https://xw7sbct9v6-1.algolianet.com/1/indexes/products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.32.1&x-algolia-application-id=XW7SBCT9V6&x-algolia-api-key=6b5e76b49705eb9f51a06d3c82f7acee'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site'
    }

    key = productName
    count = 1  # Set the number of hits per page as needed

    data = {
        'params': f'query={key}&facets=*&filters=&hitsPerPage={count}'
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if(response.status_code == 200):
        response = response.json()
        return int(response['hits'][0]['Traits'][2]["value"]), str(response['hits'][0]['Traits'][3]["value"]) # Retail Price, Release Date
    else:
        raise Exception(" Wrong status code, might be a problem with the authorization variable in headers (getProductsAndInfo.py)")