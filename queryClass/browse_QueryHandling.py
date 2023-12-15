import sys
import requests
import json
from queryHandling import QueryHandling



class BrowseQueryHandling(QueryHandling) :
    def __init__(self) :        
        super().__init__("Browse.json")
        self.size = 1
        self.page = 1
        self.productsId = None
    
    def getProductsId(self):
        if(self.response == None):
            self.getResponse()
        data = self.getResponse()['data']['browse']['results']['edges']

        self.productsId = [data[i]['node']['urlKey'] for i in range(self.size)]
        return self.productsId
        

    def setSearch(self, search, size=1, currency="GB", country="GDP") :
        self.variables['query'] = search
        self.variables['page']['limit'] = size
        self.size = size

    def writeProductId(self, categoryName):
        with open("PRODUCT_ID/" + categoryName + ".json", 'w') as file:
            json.dump(self.getProductsId(), file)

    

def main(args):
    test = BrowseQueryHandling()
    test.setSearch("nike",100)
    test.writeProductId("nike")
    
if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(args))