from fastapi import FastAPI
import requests
import json
import time
import uvicorn

with open('data.json', 'r') as file:
    detail = json.load(file)
count = 10


edge_delay=[]
client_response = {"edge_response":"","cloud_response":""}
api_response = {}
app = FastAPI()
edge_url = "http://194.199.113.43:31002/real_time"
cloud_url = "http://194.199.113.43:31001/road_side"

@app.post("/gateway")
async def decision(data: dict):
     global client_response
     global count
     global detail
    #  if count == 0:
    #      resp = requests.get(url=cloud_url+"/db_init", json={"db_ip":detail["master_ip"]})
     print (data)
     #real time communication
     t1=time.time()
     edge_response = requests.post(url=edge_url, json=data)
     t2=time.time()
     print(f"Edge server delay {(t2-t1)*1000} ms")
     if edge_response.status_code == 200:
         client_response["edge_response"] = edge_response.json()
     else:
         print(f"Something wrong with edge server: Error with {edge_response.status_code}")
     #On the fly communication
     if data["RSU"] == "interested":
         cloud_response = requests.get(url=cloud_url)
         if cloud_response.status_code == 200:
             client_response["cloud_response"] = cloud_response.json()
         else:
             print(f"Something wrong with cloud server: Error with {cloud_response.status_code}")
     else:
         client_response["cloud_response"]=""
     #client response
     return client_response


@app.post("/init")
async def set_service_endpoint(data: dict):
    global edge_url
    global cloud_url
    edge_url = data["edge_endpoint"] 
    cloud_url = data["cloud_endpoint"]
    print(f"Endpoints initialisation Done")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    print("server running")