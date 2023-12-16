from queryHandling import QueryHandling
import sys

class getMarketData_QueryHandling(QueryHandling) :
    def __init__(self, productId) :        
        super().__init__("getMarketData.json")
        self.data['variables']['productsId'] = productId
        self.response = None
        self.marketData = None

        """
        "variables": {
            "id": "adidas-yeezy-slide-slate-grey",
            "currencyCode": "GBP",
            "countryCode": "GB",
            "marketName": "GB"
        }
        """


def main(args):
    marketData = getMarketData_QueryHandling("adidas-yeezy-slide-slate-grey")
    print(marketData.getResponse())
if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(args))

