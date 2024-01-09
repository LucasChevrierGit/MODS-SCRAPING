import json
import sys
from tracemalloc import start
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import math
import requests

from queryClass.queryHandling import QueryHandling

"""
"productId": "adidas-yeezy-slide-slate-grey",
"startDate": "2022-12-14",
"endDate": "2023-12-14",
"intervals": 100,
"currencyCode": "GBP",
"isVariant": false
"""
class FetchSalesGraphQueryHandling(QueryHandling) :
    def __init__(self, productId, isVariant = False):
        super().__init__("FetchSalesGraph.json") #only open does not request 

        self.data['variables']['productId'] = productId
        self.data['variables']['isVariant'] = isVariant

        self.response = None
        self.salesGraph = None 


    def setBasicVariables(self, productId, startDate = "2022-12-14", endDate = "2023-12-14", intervals = 100):
        self.data['variables']['productsId'] = productId
        self.data['variables']['startDate'] = startDate
        self.data['variables']['endDate'] = endDate
        self.data['variables']['intervals'] = intervals

    def setCurreny(self, currencyCode = "USD"):
        self.data['variables']['currencyCode'] = currencyCode

    def responseAsPd(self):
        series = self.response['data']['product']['salesChart']['series']
        self.salesGraph = pd.DataFrame(series)
        self.salesGraph = self.salesGraph.rename(columns={'xValue': 'Date', 'yValue': 'Price'})

        self.salesGraph['Date'] = pd.to_datetime(self.salesGraph['Date'])
        self.salesGraph.set_index('Date', inplace=True)
        return self.salesGraph
    
    def responseAsPdVariant(self):
        if self.response['data']['variant']['salesChart'] == None :
            print("No data for this variant")
            return None
        series = self.response['data']['variant']['salesChart']['series']
        self.salesGraph = pd.DataFrame(series)
        self.salesGraph = self.salesGraph.rename(columns={'xValue': 'Date', 'yValue': 'Price'})

        self.salesGraph['Date'] = pd.to_datetime(self.salesGraph['Date'])
        self.salesGraph.set_index('Date', inplace=True)
        return self.salesGraph        
    
    def writeData(self, name):
        with open("./JSON/response/" + name + ".json", 'w') as file:
            self.setResponse()
            json.dump(self.response['data'], file)

    """ 
    Created to be usefull outside the class 

    intervals : number of points in the graph
    strartDate : date of the release date (format : "YYYY-MM-DD", will check sales 1 mounth prior to the release date)
    currencyCode : currency of the price

    return : a pandas dataframe with the date as index and the price as value
    """
    def fetchSalesGraph(self, intervals, startDate ,currencyCode = "USD"):

        chunk = math.floor(intervals // 500) + 1
        dates = self.chunkDate(startDate, str(date.today()), chunk)

        productId = self.data['variables']['productId']
        self.setBasicVariables(productId, startDate= dates[0].strftime('%Y-%m-%d') , endDate= dates[1].strftime('%Y-%m-%d'), intervals= int(round(intervals/chunk)))
        self.setCurreny(currencyCode= currencyCode)
        self.setResponse()

        if self.data['variables']['isVariant'] == False:
            salesGraph= self.responseAsPd() 
        else:
            salesGraph= self.responseAsPdVariant()

        for i in range(1, chunk ):
            self.setBasicVariables(productId, startDate= (dates[i] + relativedelta(days = 1)).strftime('%Y-%m-%d') , endDate= dates[i + 1].strftime('%Y-%m-%d'), intervals= int(round(intervals/chunk)))
            self.setCurreny(currencyCode= currencyCode)
            self.setResponse()
            if self.data['variables']['isVariant']:
                salesGraph = pd.concat([salesGraph,self.responseAsPdVariant()]) 
            else:
                salesGraph= pd.concat([salesGraph,self.responseAsPd()]) 
        
        print('Number of points fetched :' , salesGraph.shape[0])
        return salesGraph

    def chunkDate(self, startDate, endDate, intervals):

        start = parse(startDate)
        end = parse(endDate)

        diff = (end - start)
        interval_duration = diff / intervals  

        
        date_range = [start + i * interval_duration for i in range(intervals)]
        date_range.append(datetime.strptime(endDate, '%Y-%m-%d'))

        return date_range
    


    

def main(args):
    productIds = None
    with open("PRODUCT_ID/" + 'nike.json') as file:
        productIds = json.load(file)

    salesGraphs = [FetchSalesGraphQueryHandling(productIds[i]) for i in range(len(productIds))]
    

    for i in range(5):

        df = salesGraphs[i].responseAsPd()

        # Adding labels and title
        plt.xlabel('Date')
        plt.ylabel('Price in ' + str(salesGraphs[i].data['variables']['currencyCode']) )
        plt.title('Sales Chart')

        plt.plot(df.index, df['Price'], marker='o', linestyle='-', label = salesGraphs[i].data['variables']['productsId'])  # Plot xValue on x-axis, yValue on y-axis
        plt.legend()


    plt.show()


def main2():
    sales = FetchSalesGraphQueryHandling("8196c7f5-11f0-46aa-bd9e-75ee301d72e0")
    sales.writeData("fetchSalesGraph-adidas-yeezy-slide-slate-grey")

if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main2())