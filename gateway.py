from fastapi import FastAPI
import requests
import time
import uvicorn

area_data_endpoint=""
decision_endpoint=""
edge_delay=[]
app = FastAPI()
edge_url = "http://"+decision_endpoint+":31001/real_time"
cloud_url = "http://"+area_data_endpoint+":31002/road_side"

@app.post("/proxy")
async def decision(data: dict):
    client_response = {}
    print (data)
    #On the fly communication
    rsu_data = {"zone_indicator":data["zone_indicator"]}
    response = requests.post(url=cloud_url, json=rsu_data)
    details = response.json()
    print(type(details))
    if response.status_code == 200:
        client_response["cloud_response"] = details
    else:
        print(f"Something wrong with cloud server: Error with {details.status_code}")
    
    #real time communication
    edge_server_data={
        "front_distance":data["front_distance"],
        "details": details["crosswalk"],
        "detected": details["detected"]
        }
    t1=time.time()
    edge_response = requests.post(url=edge_url, json=edge_server_data)
    instruction = edge_response.json()
    print(instruction)
    t2=time.time()
    print(f"Edge server delay {(t2-t1)*1000} ms")
    if edge_response.status_code == 200:
        client_response["action"] = instruction["action"]
        client_response["trafic"] = instruction["trafic"]

    else:
        print(f"Something wrong with edge server: Error with {edge_response.status_code}")

    return client_response


@app.get("/init")
async def set_service_endpoint(data: dict):
    global edge_url
    global cloud_url
    edge_url = data["edge_endpoint"] 
    cloud_url = data["cloud_endpoint"]
    print(f"Endpoints initialisation Done")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    print("server running")


    


    
    

    

