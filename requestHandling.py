import sys
import requests
import json
import argparse



class BrowseQueryHandling :
    def __init__(self, path) :        
        with open(path, 'r') as file:
            self.json_data = json.load(file)
            self.cookies = self.json_data['cookies']
            self.headers = self.json_data['headers']
            self.data = self.json_data['data']
            self.compressed = self.json_data['compressed']
            self.url = self.json_data['url']
            self.method = self.json_data['method']
            self.size = 1
        self.response = None
    
    def getResponse(self) :
        if(self.response == None):
            self.response = requests.post(self.url, cookies=self.cookies, headers=self.headers, json=self.data).json()
        return self.response
    
    def getProductsId(self):
        if(self.response == None):
            self.getResponse()
        data = self.getResponse()['data']['browse']['results']['edges']

        return [data[i]['node']['urlKey'] for i in range(self.size)]
        
        

    def setSearch(self, search, size=1, currency="GB", country="GDP") :
        self.data['variables']['query'] = search
        self.data['variables']['page']['limit'] = size
        self.size = size

    


def main(args):
    test = BrowseQueryHandling("./JSON/query/Browse.json")
    test.setSearch("nike",100)
    print(test.getProductsId())


    
if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(args))