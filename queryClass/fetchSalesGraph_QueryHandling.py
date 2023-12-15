import json
from queryHandling import QueryHandling

class FetchSalesGraphQueryHandling(QueryHandling) :
    def __init__(self, productId):
        super().__init__("FetchSalesGraph.json")
        self.productsId = self.json_data['variables']['productsId']
        self.startDate = self.json_data['variables']['startDate']
        self.endDate = self.json_data['variables']['endDate']
        self.intervals = self.json_data['variables']['intervals']
        self.currencyCode = self.json_data['variables']['currencyCode']
        self.isVariant = self.json_data['variables']['isVariant']
        self.productId = productId
        self.response = None
        self.salesGraph = None