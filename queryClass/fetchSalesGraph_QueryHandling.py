import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

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
    def __init__(self, productId):
        super().__init__("FetchSalesGraph.json") #only open does not request 
        self.data['variables']['productsId'] = productId

        self.response = None
        self.salesGraph = None 

        """
            self.data['variables']['productsId']
            self.data['variables']['startDate']
            self.data['variables']['endDate']
            self.data['variables']['intervals']
            self.data['variables']['currencyCode']
            self.data['variables']['isVariant']
            self.data['variables']['startDate']
        """


    def setBasicVariables(self, productId, startDate = "2022-12-14", endDate = "2023-12-14", intervals = 100):
        self.data['variables']['productsId'] = productId
        self.data['variables']['startDate'] = startDate
        self.data['variables']['endDate'] = endDate
        self.data['variables']['intervals'] = intervals

    def setCurreny(self, currencyCode = "USD"):
        self.data['variables']['currencyCode'] = currencyCode

    def responseAsPd(self):
        series = self.getResponse()['data']['product']['salesChart']['series']

        self.salesGraph = pd.DataFrame(series)
        self.salesGraph = self.salesGraph.rename(columns={'xValue': 'Date', 'yValue': 'Price (' + str(self.data['variables']['currencyCode']) + ')'})
        self.salesGraph['Date'] = pd.to_datetime(self.salesGraph['Date'])
        self.salesGraph.set_index('Date', inplace=True)
        return self.salesGraph
    
    def writeData(self, name):
        with open("./JSON/response/" + name + ".json", 'w') as file:
            json.dump(self.getResponse()['data'], file)

    def chunkDate(startDate, endDate, intervals):

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
        df['xValue'] = pd.to_datetime(df['xValue'])

        # Adding labels and title
        plt.xlabel('Date')
        plt.ylabel('Price in ' + str(salesGraphs[i].data['variables']['currencyCode']) )
        plt.title('Sales Chart')

        plt.plot(df['xValue'], df['yValue'], marker='o', linestyle='-', label = salesGraphs[i].data['variables']['productsId'])  # Plot xValue on x-axis, yValue on y-axis
        plt.legend()


    plt.show()


def main2():
    sales = FetchSalesGraphQueryHandling("8196c7f5-11f0-46aa-bd9e-75ee301d72e0")
    sales.writeData("fetchSalesGraph-adidas-yeezy-slide-slate-grey")

if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main2())