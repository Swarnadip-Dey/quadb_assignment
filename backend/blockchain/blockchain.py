import time
from blockchain.block import Block  # Import the Block class
from database import db_manager

class Blockchain:
    def __init__(self, difficulty=4):
        # Initialize the blockchain with the genesis block
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        # "genesis block"
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, new_block):
        # Add a new block to the chain after mining it
        new_block.previous_hash = self.chain[-1].hash  # Set the previous hash
        new_block.mine_block(self.difficulty)  # Mine the block before adding it
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain by checking hashes
        and ensuring the previous hash in each block is correct.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash matches the calculated hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} is tampered!")
                print(f"Stored Hash: {current_block.hash}")
                print(f"Calculated Hash: {current_block.calculate_hash()}")
                return False

            # Check if the current block's previous_hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index} is tampered!")
                print(f"Stored Previous Hash: {current_block.previous_hash}")
                print(f"Previous Block's Hash: {previous_block.hash}")
                return False

        print("Blockchain is valid.")
        return True

    def get_all_blocks(self):
        # Return a list of all blocks in the blockchain, converted to dictionaries
        return [block.to_dict() for block in self.chain]

    def get_block(self, index):
        """
        Retrieve a block by its index.
        Returns None if the index is out of bounds.
        """
        if index < 0 or index >= len(self.chain):
            return None
        return self.chain[index]

    def mine_block(self):
        """
        Mines a new block with transactions from the database and adds it to the blockchain.
        It also removes the mined transactions from the database.
        """
        # Ensure the chain is valid before mining a new block
        if not self.is_chain_valid():
            raise ValueError("Blockchain is invalid. Mining aborted.")

        # Get pending transactions from the database
        transactions = db_manager.get_all_transactions()
        transaction_data = [trans['transaction_data'] for trans in transactions]

        # Create and mine the new block
        block = Block(len(self.chain), time.time(), transaction_data, self.chain[-1].hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # Remove the transactions from the database after mining
        for transaction in transactions:
            db_manager.delete_transaction(transaction['id'])
