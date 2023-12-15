import json
import requests

class QueryHandling :
    def __init__(self, queryName) :        
        with open("./JSON/query/" + str(queryName), 'r') as file:
            self.json_data = json.load(file)
            self.cookies = self.json_data['cookies']
            self.headers = self.json_data['headers']
            self.data = self.json_data['data']
            self.variables = self.data['variables']
            self.compressed = self.json_data['compressed']
            self.url = self.json_data['url']
            self.method = self.json_data['method']
            self.operationName = self.data['operationName']
            self.response = None
            
    
    def setHeadersAuthVariable(self, device_id, session_id, authorization) :
        self.headers['device_id'] = device_id
        self.headers['session_id'] = session_id
        self.headers['authorization'] = authorization

    def getResponse(self) :
        if(self.response == None):
            self.response = requests.post(self.url, cookies=self.cookies, headers=self.headers, json=self.data)
            print(self.operationName + " query, status code :",self.response.status_code)
            if(self.response.status_code == 200):
                return self.response.json()
            else:
                raise Exception(" Wrong status code, might be a problem with the authorization variable in headers")
            
        return self.response.json()