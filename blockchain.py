# Modified from https://medium.com/pythoneers/building-a-blockchain-from-scratch-with-python-489e7116142e

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
    
    def __str__(self) -> str:
        return f"Block #{self.block_id}\nTimestamp: {self.timestamp}\nData: {self.data}\nHash: {self.hash}\nPrevious Hash: {self.previous_hash}\n"

class Blockchain:
    def __init__(self) -> None:
        self.date_format = "%Y-%m-%d %H:%M:%S.%f"
        self.chain = [self.create_genesis_block()]

    def __iter__(self):
        self.current_block_id = 0
        return self
    
    def __next__(self):
        if self.current_block_id < len(self.chain):
            current_block = self.chain[self.current_block_id]
            self.current_block_id += 1
            return current_block
        else:
            raise StopIteration

    def create_genesis_block(self) -> Block:
        return Block(0, date.now(), [], "0")
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_block(self, timestamp, data) -> bool:
        try:
            date.strptime(str(timestamp), self.date_format)
        except ValueError:
            return False

        if not isinstance(data, Data):
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

            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
