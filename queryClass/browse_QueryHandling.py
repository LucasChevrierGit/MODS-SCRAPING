import sys
import requests
import json
from queryHandling import QueryHandling



class BrowseQueryHandling(QueryHandling) :
    def __init__(self) :        
        super().__init__("Browse.json")
        self.productsId = None
    
    def getProductsId(self):
        if(self.response == None):
            self.getResponse()
        data = self.getResponse()['data']['browse']['results']['edges']

        self.productsId = [data[i]['node']['urlKey'] for i in range(self.data['variables']['page']['limit'])]
        return self.productsId
        
    def setSearch(self, search, size=1, currency="GB", country="GDP") :
        self.data['variables']['query'] = search
        self.data['variables']['page']['limit'] = size

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