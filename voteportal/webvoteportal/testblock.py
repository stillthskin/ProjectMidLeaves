#!/usr/bin/env python3
import datetime
import hashlib
import json
from models import Profile, constestant
#from flask import Flask, jsonify


class Blockchain:
    #Blockchain Build
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash="0", thedata={})
    
    def create_block(self, proof, prev_hash,thedata):
        block = {'index':len(self.chain)+1, 
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'prev_hash':prev_hash,
                 'data':thedata}
        self.chain.append(block)
        return block
    
    def get_last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #problem definition for the miners.
            hash_orp = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()#le problem()
            if hash_orp[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hassher(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hassher(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_orp = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_orp != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
    def chain_data(self):
        datadict = {}
        data = constestant.objects.all()
        for i in data:
        
            print(i.fname,i.votes)
            datadict[i.fname] = i.votes
        print(datadict)
        context = {
        "datadict":datadict
         }
        return datadict
       
#Blockchain Mine 
#app = Flask(__name__)

blockchain = Blockchain()

#@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_last_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hassher(prev_block)
    thedata = blockchain.chain_data()
    block = blockchain.create_block(proof, previous_hash) 
    response = {'message' : 'Congrats block mined',
                'index':block['index'],
                'proof': block['proof'],
                'previous_hash':block['prev_hash'],
                'data':thedata
                  }
    #return jsonify(response), 200
    return response

#@app.route('/get_chain', methods=['GET']) 
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    #return jsonify(response), 200
    return response

#@app.route('/is_chain', methods=['GET']) 
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Chain is valid'} 
    else:
        response = {'message':'chain is invalid'}
    
    #return jsonify(response), 200
    return response
mine_block()
#app.run(host = '0.0.0.0', port = 5000