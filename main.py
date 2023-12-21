
from queryClass.getMarketData_QueryHandling import GetMarketData_QueryHandling
from queryClass.fetchSalesGraph_QueryHandling import FetchSalesGraphQueryHandling
from queryClass.getProductsAndInfo import getRetailPrice_ReleaseDate

import json
import matplotlib.pyplot as plt
import pandas as pd
import math


""" 
    category name : name of the json file in PRODUCT_ID folder
    size : number of shoes to check

    returns a list of tuples (product_id, urlKey) of the shoes that are not variants of other listed shoes

    En réalité les variants, c'est les id de paires pour des tailles différente, c'est pas des paires de couleurs différentes ou quoi
    On pourrait filtrer les paires sorties le meme jour pour avoir moins de correlation 
"""
def filterVariants(categoryName, size= None):
    productIds = None

    with open("PRODUCT_ID/" + categoryName + '.json') as file:
        productIds = json.load(file)

    if size == None:
        size = len(productIds)
        
    variant_ids_set = set()

    filtered_id = []

    for i in range(size):
        marketData = GetMarketData_QueryHandling(productIds[i])
        product_id = marketData.getResponse()['data']['product']['id']
        urlKey = marketData.getResponse()['data']['product']['urlKey']
        print("title : ", urlKey)
        variant_ids = [ variant['id'] for variant in marketData.getResponse()['data']['product']['variants']]

        if product_id not in variant_ids_set:
            filtered_id.append((product_id , urlKey))

        # Update the variant_ids_set with the current variant_ids
        variant_ids_set.update(variant_ids)

    return filtered_id


""" 
    category name : name of the json file in PRODUCT_ID folder
    size : number of shoes to get sales if None then all  
    return all sales graph as pd
"""

def fetchSalesGraph(urlKey, intervals = 1000 , currencyCode = "USD"):

    sales = FetchSalesGraphQueryHandling(urlKey)
    salesGraph = None

    releaseDate = str(getRetailPrice_ReleaseDate(urlKey)[1])
    dt = parse(releaseDate)
    dt = dt - relativedelta(months=1)
    releaseDate = dt.strftime('%Y-%m-%d')
    chunk = math.floor(intervals // 500) + 1
    print(chunk)


    dates = chunkDate(releaseDate, str(date.today()), chunk)

    sales.setBasicVariables(urlKey, startDate= dates[0].strftime('%Y-%m-%d') , endDate= dates[1].strftime('%Y-%m-%d'), intervals= int(round(intervals/chunk)))
    sales.setCurreny(currencyCode= currencyCode)
    sales.setResponse()
    salesGraph= sales.responseAsPd() 

    for i in range(1, chunk ):
        sales.setBasicVariables(urlKey, startDate= (dates[i] + relativedelta(days = 1)).strftime('%Y-%m-%d') , endDate= dates[i + 1].strftime('%Y-%m-%d'), intervals= int(round(intervals/chunk)))
        sales.setCurreny(currencyCode= currencyCode)
        sales.setResponse()
        
        salesGraph = pd.concat([salesGraph,sales.responseAsPd()]) 

    print(salesGraph.shape)


    return salesGraph


from datetime import date, datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta



def chunkDate(startDate, endDate, intervals):
    start = parse(startDate)
    end = parse(endDate)

    diff = (end - start)
    interval_duration = diff / intervals  

    
    date_range = [start + i * interval_duration for i in range(intervals)]
    date_range.append(datetime.strptime(endDate, '%Y-%m-%d'))

    return date_range


with open("PRODUCT_ID/" + 'Jordan1' + '.json') as file:
        productIds = json.load(file)


urlKey = productIds[0]
print(urlKey)

salesGraph = fetchSalesGraph(urlKey, intervals = 500, currencyCode="USD")
plt.plot(salesGraph)
plt.show()

salesGraph.to_csv("SALES/variants.csv")
