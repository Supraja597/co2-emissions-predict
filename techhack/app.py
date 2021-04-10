
from flask import Flask, request,  render_template
import requests

import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY="-Lh-yoAia6zoIt2PXGDC2PNRtAS8KOUNPFTg_Yzw_5Ss"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [], "values": []}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7b6e728b-0a52-454b-b0b6-8ceeebb21ca2/predictions?version=2021-04-09', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    Year = request.form["Year"]
    CarName = request.form["CarName"]
    Model = request.form["Model"]
    EngineSize = request.form["EngineSize"]
    Cylinders = request.form["Cylinders"]
   
    FuelType = request.form["FuelType"]
    FuelConsumption = request.form["FuelConsumption"]
    


    t = [[int(Year),CarName,Model,int(EngineSize),int(Cylinders),FuelType,int(FuelConsumption)]]
    payload_scoring = {"input_data": [ {"field": ["Year","CarName","Model","EngineSize","Cylinders","FuelType","FuelConsumption"],"values": t}]}
    print(t)
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b3f12d8a-374d-4f31-8a16-bf21bd16f6ee/predictions?version=2021-04-10')
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    
    return render_template('index1.html', prediction_text= pred)


if __name__ == "__main__":
    app.run()
