from queryClass.queryHandling import QueryHandling
import sys

class GetMarketData_QueryHandling(QueryHandling) :
    def __init__(self, productId) :        
        super().__init__("getMarketData.json")
        self.data['variables']['id'] = productId


        """
        "variables": {
            "id": "adidas-yeezy-slide-slate-grey",
            "currencyCode": "GBP",
            "countryCode": "GB",
            "marketName": "GB"
        }
        """


def main(args):
    marketData = GetMarketData_QueryHandling("adidas-yeezy-slide-slate-grey")
    print(marketData.getResponse())
if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(args))

