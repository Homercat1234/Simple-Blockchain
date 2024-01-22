from datetime import datetime as date
import hashlib

class Data:
    def __init__(self, sender, message) -> None:
        self.sender = sender
        self.message = message
    
    def __str__(self) -> str:
        return(f'{self.sender}, {self.message}')

class Block:
    def __init__(self, block_id, timestamp, data, previous_hash) -> None:
        self.block_id = block_id
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        hash_string = str(self.block_id) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(hash_string.encode()).hexdigest()

class Blockchain:
    def __init__(self) -> None:
        self.date_format = "%Y-%m-%d %H:%M:%S.%f"
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        return Block(0, date.now(), [], "0")
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_block(self, timestamp, data) -> bool:
        try:
            date.strptime(str(timestamp), self.date_format)
        except ValueError:
            return False

        new_block = Block(len(self.chain), str(timestamp), data, self.get_latest_block().hash)
        self.chain.append(new_block)
        
        return True

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if(current_block.previous_hash != previous_block.hash):
                return False
            
        return True
    
    def print_chain(self) -> None:
        for block in self.chain:
            print("Block #" + str(block.block_id))
            print("Timestamp: " + str(block.timestamp))
            print("Data: " + str(block.data))
            print("Hash: " + block.hash)
            print("Previous Hash: " + block.previous_hash)
            print("\n")
