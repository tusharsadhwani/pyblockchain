import hashlib
import json
import requests
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, abort, jsonify, request, redirect
from flask_cors import CORS

class Blockchain:
    def __init__(self):
        self.chain = []
        self.new_block()

    def new_block(self):
        index = len(self.chain) + 1
        data = ''
        nonce = 0
        last_block = blockchain.chain[-1] if len(self.chain) else None
        previous_hash = last_block['hash'] if last_block else '0'

        block = {
            'index': index,
            'timestamp': time(),
            'data': data,
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        self.chain.append(block)
        self.calculate_hash(index)
        self.validate_block(index)
    
    def mine(self, index):
        block = self.chain[index-1]
        nonce = 0

        while not self.validate_hash(index, nonce=nonce):
            nonce += 1
        
        block['nonce'] = nonce
        self.calculate_and_validate_all_blocks(index)

    def validate_hash(self, index, nonce=None):
        block = self.chain[index-1]
        data = block['data']
        prev_hash = block['previous_hash']
        if nonce is None:
            nonce = block['nonce']
        return Blockchain.hash(index, data, prev_hash, nonce)[:4] == '0000'
    
    def change_data(self, index, data):
        block = self.chain[index-1]
        block['data'] = str(data)
        self.calculate_and_validate_all_blocks(index)
    
    def change_nonce(self, index, nonce):
        block = self.chain[index-1]
        block['nonce'] = str(nonce)
        self.calculate_and_validate_all_blocks(index)
    
    def calculate_hash(self, index):
        block = self.chain[index-1]
        data = block['data']
        nonce = block['nonce']

        previous_block = self.chain[index-2] if (len(self.chain) > 1 and index > 1) else None
        previous_hash = previous_block['hash'] if previous_block else '0'

        new_block_hash = Blockchain.hash(index, data, previous_hash, nonce)
        block['hash'] = new_block_hash

    def validate_block(self, index):
        block = self.chain[index-1]

        previous_block = self.chain[index-2] if (len(self.chain) > 1 and index > 1) else None
        block['previous_hash'] = previous_block['hash'] if previous_block else '0'

        block['validated'] = self.validate_hash(index)

    def calculate_and_validate_all_blocks(self, index):
        for i in range(index, len(self.chain)+1):
            self.calculate_hash(i)
            self.validate_block(i)

    @staticmethod
    def hash(index, data, prev_hash, nonce):
        return hashlib.sha1((str(index)+data+prev_hash+str(nonce)).encode()).hexdigest()


app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/newblock', methods=['GET'])
def new_block():
    blockchain.new_block()
    return redirect('/chain')

@app.route('/mine/<int:index>', methods=['GET'])
def mine(index):
    blockchain.mine(index=index)
    return redirect('/chain')

@app.route('/changedata/<int:index>', methods=['GET'])
def change_data(index):
    values = request.args
    print(values)
    required = ['data']
    for k in required:
        if k not in values:
            return abort(400)

    data = values['data']
    blockchain.change_data(index, data)

    return redirect('/chain')

@app.route('/changenonce/<int:index>', methods=['GET'])
def change_nonce(index):
    values = request.args
    print(values)
    required = ['nonce']
    for k in required:
        if k not in values:
            return abort(400)

    nonce = values['nonce']
    blockchain.change_nonce(index, nonce)

    return redirect('/chain')

@app.route('/clear', methods=['GET'])
def clear_blockchain():
    blockchain.__init__()
    return redirect('/chain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
