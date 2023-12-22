import json
import requests

class QueryHandling :
    def __init__(self, queryName) :        
        with open("./JSON/query/" + str(queryName), 'r') as file:
            self.json_data = json.load(file)
            self.cookies = self.json_data['cookies']
            self.headers = self.json_data['headers']
            self.data = self.json_data['data']

            self.url = self.json_data['url']
            self.operationName = self.data['operationName']
            self.response = None
            
    
    def setHeadersAuthVariable(self, device_id, session_id) :
        self.headers['device_id'] = device_id
        self.headers['session_id'] = session_id

    def getResponse(self) :
        if(self.response == None):
            self.response = requests.post(self.url, cookies=self.cookies, headers=self.headers, json=self.data)
            print(self.operationName + " query, status code :",self.response.status_code)
            if(self.response.status_code == 200):
                self.response = self.response.json()
                return self.response
            else:
                print(" Wrong status code for " + self.operationName + ", might be a problem with the authorization variable in headers")
                response = input('Check on stockX.com if there is a capcha. type "yes" to retry')
                if response == "yes":
                    self.response = None
                    return self.getResponse()
                else :
                    raise Exception("Problem not solved")
            
        return self.response
    
    def setResponse(self) :
        self.response = requests.post(self.url, cookies=self.cookies, headers=self.headers, json= self.data)
        print(self.operationName + " query, status code :",self.response.status_code)
        if(self.response.status_code == 200):
            self.response = self.response.json()
        else:
            print(" Wrong status code for " + self.operationName + ", might be a problem with the authorization variable in headers")
            print(self.response)
            response = input('Check on stockX.com if there is a capcha. type "yes" to retry')
            if response == "yes":
                self.response = self.getResponse()
            else :
                raise Exception("Problem not solved")
        
    
    def changeHeadersId(self, device_id, session_id):
        self.headers['x-stockx-device-id'] = device_id
        self.headers['x-stockx-session-id'] = session_id

    def writeData(self, name):
        with open("./JSON/response/" + name + ".json", 'w') as file:
            json.dump(self.getResponse(), file)




if __name__ == '__main__':
    productPriceLvl = QueryHandling("getProductMarketSales.json")
    productPriceLvl.getResponse()
    productPriceLvl.writeData("getProductMarketSales")
