import sys
import requests
import json
import pandas as pd
from queryClass.queryHandling import QueryHandling



class BrowseQueryHandling(QueryHandling) :
    def __init__(self) :        
        super().__init__("Browse.json")
        self.productsId = None
    
    """ 
    Set the parameter in the JSON query 
    
    search : the element you want to search on stockX (ie : 'nike air max')
    size : Number of shoe pair the query returns
    gender : ""/"men"/"women"
    years : release date of the shoes 
    sort ID : Can check all sort id type in JSON\response\browseSort.json 
    shoeSize : adding shoe size modify the returned json, don't try getProductId with it ( shoeSize = ['9.5'])
    """
    def setSearch(self, search, size=1, gender = "men", years = ["2021","2022"], sortID = "featured", shoeSize = ['']) :
        self.data['variables']['query'] = search
        self.data['variables']['page']['limit'] = size
        self.data['variables']['filters'][1]['selectedValues'][0] = gender
        self.data['variables']['filters'][2]['selectedValues'] = years
        self.data['variables']['sort']['id'] = "featured"
        if len(shoeSize) != 0 :
            self.data['variables']['filters'][3]['selectedValues'] = shoeSize

    """can check all country code in JSON\response\currencyAndCountry.json"""
    def setCountry(self, currency = "USD", country = "US", marketName = "US"):
        self.data['variables']['currency'] = currency
        self.data['variables']['country'] = country
        self.data['variables']['marketName'] = marketName

    def writeProductId(self, categoryName):
        with open("PRODUCT_ID/" + categoryName + ".json", 'w') as file:
            json.dump(self.getProductsId(), file)
    def writeData(self, name):

        with open("./JSON/response/" + name + ".json", 'w') as file:
            json.dump(self.getResponse()['data'], file)

    def getProductsId(self):
        if(self.response == None):
            self.getResponse()
        data = self.getResponse()['data']['browse']['results']['edges']

        self.productsId = [data[i]['node']['urlKey'] for i in range(len(data))]
        return self.productsId
    
    def getInfo_DF(self):

        self.setResponse()
        resp = self.getResponse()['data']['browse']['results']['edges']
        ids = []  
        url_keys = []
        retailPrice = []
        releaseDate = []
        variants = []
        sold = []
        averagePrice = []
        image = ""

        for shoe in resp :
            ids.append(shoe["objectId"])
            node = shoe["node"]
            url_keys.append(node['urlKey'])

            image = node['media']['thumbUrl']

            index = image.find(".jpg")
            image = image[:index + len(".jpg")]
            if len(node["productTraits"]) != 2 :
                print("WARNING : " + node['urlKey'] + " has less than 2 product traits")
                print(node["productTraits"])
                retailPrice.append(node["productTraits"][0]["value"])
                releaseDate.append(None)
                print(node)
            else :
                retailPrice.append(node["productTraits"][0]["value"])
                releaseDate.append(node["productTraits"][1]["value"])
            variants.append( { variant['traits']['size'] : variant['id']  for variant in node['variants']})
            sold.append( node['market']['deadStock']['sold'])
            averagePrice.append( node['market']['deadStock']['averagePrice'])

        data = {
            'ID': ids,
            'URL Key': url_keys,
            'retail Price': retailPrice,
            'release Date': releaseDate,
            'sold' : sold,
            'average price' : averagePrice,
            'image' : image,
            'Variants': variants

        }
        return pd.DataFrame(data)



    

def main(args):
    test = BrowseQueryHandling()
    test.setSearch("adidas-yeezy-boost-350", 10 , gender = "men", years = ["2021","2022"], sortID = "featured")
    test.getResponse()

    df = test.getInfo_DF()

    """ Save most of the data from the browser query as csv """
    df.to_csv('./INFO_BROWSE/adidas-yeezy-boost-350_10.csv')

    """ List the number of shoe sold for a specific size 
    checkVariantId = 0 
    for key in df['Variants'][checkVariantId].keys():
        
        test.setSearch(df.iloc[0]['URL Key'], 1, shoeSize= [key])
        index = 0
        test.setResponse()
        print('size : ', key , ', total sold : ', test.getResponse()['data']['browse']['results']['edges'][index]['node']['market']['deadStock']['sold'])

    """    
if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(args))


