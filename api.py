from flask import Flask
from flask import request, url_for
from flask import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlitedb import create_connection,create_table,main
import sqlite3

import json
from datetime import datetime
app = Flask(__name__)

class WalletTransactions():
    def __init__(self):
        self.database_file = "Downloads\\pythonsqlite-assignment.db"
        
    
    def create_wallets(self,id,balance,coin_symbol):
        try:
            conn = sqlite3.connect(self.database_file)
            c = conn.cursor()
            query = "INSERT INTO wallet (id,balance,coin_symbol) VALUES ({id}, {balance}, '{coin_symbol}' )".\
            format(id=id, balance=balance, coin_symbol=coin_symbol)
            print(query)
            c.execute(query)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column ')

        
    def get_wallets(self,id):
        try:
            conn = sqlite3.connect(self.database_file)
            c = conn.cursor()
            query = "SELECT * FROM  wallet where id = {id}".\
            format(id=id)
            print(query)
            c.execute(query)
            all_rows = c.fetchall()
            #print(all_rows[0][1])
            conn.close()
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column')

        return all_rows
    
    def delete_wallets(self,id):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        query = "DELETE FROM  wallet where id = {id}".\
        format(id=id)
        conn.close()
        return "success"
    
    '''
    def update_wallets(self,id, amount,action):
        session = self.session_factory()
        wallets = session.query(Wallet).filter_by(id=id).first()
        if action == "add":
            wallets.balance = (wallets.balance + int(amount))
        else:
            wallets.balance = (wallets.balance - int(amount))
        session.commit()
        session.close()
        return "success"

    def create_transaction(self,from_wallet,to_wallet,amount,time_stamp,txn_hash):
        session = self.session_factory()
        self.update_wallets(from_wallet,amount,"subtract")
        self.update_wallets(to_wallet,amount,"add")
        #time_stamp = datetime(2012, 3, 3, 10, 10, 10)
        transaction = Transaction(from_wallet_id=from_wallet,to_wallet_id=to_wallet,amount=int(amount),time_stamp = time_stamp,txn_hash = txn_hash, status ="Pending")
        session.add(transaction)
        session.commit()
        session.close()

    def get_transaction(self,txn_hash):
        session = self.session_factory()
        tran_query = session.query(Transaction).filter_by(txn_hash=txn_hash).first()
        session.close()
        return tran_query
    '''
@app.route('/')
def index():
    return 'OK'

# TODO add all routes here!
@app.route('/wallets/<id>', methods=['GET'])
def get_wallet_details(id): 
    wt = WalletTransactions() 
    result = wt.get_wallets(id)
    print(result)
    if result == None:
        resp = "Id does not exist"
    else:
        resp = {'id': result[0][0],'balance': result[0][1], 'coin_symbol': result[0][2]}
        
    js = json.dumps(resp)
    return Response(js,status=200,mimetype='text/json')

@app.route('/wallets', methods=['POST'])
def post_wallet_details(): 
    content = request.get_json(force=True)
    wt = WalletTransactions() 
    wt.create_wallets(int(content['id']),int(content['balance']),content['coin_symbol'])
    return Response(status=201,mimetype='application/json')

@app.route('/wallets/<id>', methods=["DELETE"])
def delete_wallet_details(id):
    wt = WalletTransactions() 
    wt.delete_wallets(id)
    return Response(status=200)

@app.route('/txns', methods=['POST'])
def post_transactions_details(): 
    content = request.get_json(force=True)
    wt = WalletTransactions() 
    # get all details from post request
    from_wallet = content['from_wallet']
    to_wallet = content['to_wallet']
    amount = content['amount']
    time_stamp = datetime.strptime(content['time_stamp'], "%Y-%m-%d %H:%M:%S.%f")
    txn_hash = content['txn_hash']
    
    #check if the from_wallet and to_wallet exist, if not then create one
    result_from_wallet = wt.get_wallets(int(from_wallet))
    if result_from_wallet == None:
        return Response("from wallet does not exist",status = 400,mimetype='application/json')
    else:
        coin_symbol = result_from_wallet.coin_symbol


    result_to_wallet = wt.get_wallets(int(to_wallet))
    print(result_to_wallet)
    if result_to_wallet == None:
        wt.create_wallets(int(to_wallet),0,coin_symbol)
        
        
    wt.create_transaction(int(from_wallet),int(to_wallet),int(amount),time_stamp,txn_hash)
    return Response(status=201,mimetype='application/json')


@app.route('/txns/<tran_hash>', methods=['GET'])
def get_transaction_details(tran_hash): 
    wt = WalletTransactions() 
    result = wt.get_transaction(tran_hash)
    print(result)
    if result == None:
        resp = "transaction does not exist"
    else:
        resp = {'status': result.status,'from_wallet': result.from_wallet_id, 'to_wallet': result.to_wallet_id,'amount':result.amount,'time_stamp':str(result.time_stamp),'txn_hash':result.txn_hash}
    js = json.dumps(resp)
    return Response(js,status=200,mimetype='text/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
    
    