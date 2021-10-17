pip install flask

# Importing the libraries
from flask import Flask, request
import datetime

# Inititating the Flask App
app = Flask(__name__)

# In memory points data
points_data = []


# Route to add transaction
@app.route('/add_transaction',methods=['GET'])
def add_tx():
    payer = request.args['payer']
    points = request.args['points']
    timestamp = request.args['timestamp']
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    points_data.append({'payer':payer,'points':float(points),'timestamp':timestamp})
    print(points_data)
    return {'Status':'OK'}



# Route to spend points
@app.route('/spend_points',methods=['GET'])
def spend_balance():
    points = float(request.args['points'])
    sorted_txs = (sorted(points_data,key=lambda d: d['timestamp']))
    resp_dict = []
    for tx in sorted_txs:
        if points<tx['points']:
            new_points = tx['points'] - points
            payer = tx['payer']
            timestamp = tx['timestamp']
            points_data.remove(tx)
            points_data.append({'payer':payer, 'points':new_points,'timestamp':timestamp})
            resp_dict.append({'payer':payer, 'points':-1*points})
            break
        elif points==tx['points']:
            payer = tx['payer']
            timestamp = tx['timestamp']
            points_data.remove(tx)
            resp_dict.append({'payer':payer, 'points':-1*points})
            break
        elif points>tx['points']:
            if tx['points']>0:
                new_points = 0 
                payer = tx['payer']
                timestamp = tx['timestamp']
                points_data.remove(tx)
                points_data.append({'payer':payer, 'points':new_points,'timestamp':timestamp})
                resp_dict.append({'payer':payer, 'points':-1*tx['points']})
                points -= tx['points']
    return {'response':resp_dict}


# Route to get balance
@app.route('/get_balance',methods=['GET'])
def get_balance():
    all_payers = list(set([x['payer'] for x in points_data]))
    resp = {}
    for p in all_payers:
        resp[p] = 0
        for tx in points_data:
            if tx['payer']==p:
                resp[p] += tx['points']
    return resp



if __name__=='__main__':
    app.run()
    

