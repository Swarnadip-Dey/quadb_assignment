import time
import threading
import os
import signal
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from blockchain.blockchain import Blockchain
from database import db_manager

SECRET_TAMPER_PATH = "/tamper-secret"  # Endpoint for tampering blocks

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set mining difficulty
MINING_DIFFICULTY = 4
blockchain = Blockchain(difficulty=MINING_DIFFICULTY)

db_manager.create_transactions_table()  # Initialize transaction table

# Background Mining Thread
mining_active = True

def mine_continuously():
    """
    Continuously mines new blocks in the background.
    Stops mining if an error occurs, and triggers server shutdown.
    """
    global mining_active
    while mining_active:
        try:
            blockchain.mine_block()
            print(f"Mined new block at {time.time()}")
        except ValueError as e:
            print(f"Mining aborted: {e}")
            mining_active = False  # Stop the mining thread
            trigger_shutdown()  # Shutdown Flask server on error
        time.sleep(10)

def trigger_shutdown():
    """
    Triggers the Flask server shutdown by sending an internal request to the shutdown route.
    """
    print("Shutting down the server via internal request...")
    try:
        requests.post("http://localhost:5000/shutdown")  # Internal request to stop Flask
    except requests.exceptions.RequestException as e:
        print(f"Shutdown request failed: {e}")
        os._exit(1)  # Force exit if the shutdown request fails

# Start mining thread
if mining_active:
    mining_thread = threading.Thread(target=mine_continuously, daemon=True)
    mining_thread.start()

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """
    Returns the entire blockchain.
    
    """
    return jsonify(blockchain.get_all_blocks()), 200


@app.route('/transactions', methods=['POST'])
def add_transactions():
    """
    Adds multiple transactions to the pending transactions database.
    
    """
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Must be a list of transactions.'}), 400

    for transaction in data:
        if not isinstance(transaction, str):
            return jsonify({'message': 'Invalid transaction data. Must be a list of strings.'}), 400

        db_manager.insert_transaction(transaction)

    return jsonify({'message': f'{len(data)} transactions added to pending transactions'}), 201

@app.route(f'{SECRET_TAMPER_PATH}/<int:index>', methods=['POST'])
def tamper_block(index):
    """
    Tamper with a block by appending a tampered transaction.
    """
    try:
        block = blockchain.get_block(index)
        if not block:
            return jsonify({'message': 'Block not found'}), 404

        block.transactions.append("Tampered Transaction")
        return jsonify({'message': f'Block {index} tampered successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error tampering block: {str(e)}'}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Gracefully shuts down the Flask server, stops mining, and waits for mining thread to finish.
    """
    print("Flask server is shutting down...")
    global mining_active
    mining_active = False  # Stop the mining thread
    mining_thread.join()  # Wait for the mining thread to finish
    os.kill(os.getpid(), signal.SIGINT)  # Send termination signal to stop the server
    return jsonify({'message': 'Server is shutting down due to mining failure'}), 200

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Server interrupted, shutting down...")
        mining_active = False  # Stop the mining thread
        mining_thread.join()  # Wait for the mining thread to finish
        os._exit(1)  # Force exit on Ctrl+C
