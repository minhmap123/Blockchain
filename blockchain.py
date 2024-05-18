import hashlib
import json
import datetime 

class Block:   
    """
    This is a class representing a single block in the blockchain.
    
    Attributes:
        index (int): The position of the block in the blockchain.
        timestamp (datetime): The time at which the block was created.
        data (any): The data stored in the block, typically a transaction or asset information.
        prev_hash (str): The hash of the previous block in the blockchain.
        hash (str): The hash of the current block.
        nonce (int): The nonce used for the proof-of-work.
    """
    
    def __init__(self, index : int, timestamp, data : any, prev_hash : str, nonce=0) -> None:
        """
        The constructor for the Block class.
        
        Parameters:
            index (int): The position of the block in the blockchain.
            timestamp (datetime): The time at which the block was created.
            data (any): The data stored in the block.
            prev_hash (str): The hash of the previous block in the blockchain.
            nonce (int): The nonce used for the proof-of-work.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Computes the SHA-256 hash of the block's contents.
        
        Returns:
            str: The computed hash as a hexadecimal string.
        """
        hash_string = (str(self.index) + str(self.timestamp) + str(self.data) + self.prev_hash + str(self.nonce))
        return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mines the block by finding a hash with a certain number of leading zeros.

        Parameters:
            difficulty (int): The number of leading zeros required in the hash.
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the block.
        
        Returns:
            str: A formatted string describing the block.
        """
        return (f"Block #{self.index}\n"
                f"\tTimestamp    : {self.timestamp}\n"
                f"\tData         : {self.data}\n"
                f"\tPrevious Hash: {self.prev_hash}\n"
                f"\tBlock Hash   : {self.hash}\n"
                f"\tNonce        : {self.nonce}\n")
    
class Transaction: 
    """
    This is a class representing a transaction between two parties.
    
    Attributes:
        owner (str): The sender of the transaction.
        buyer (str): The receiver of the transaction.
        asset_name (str): The name of the asset being transferred.
        count (int): The quantity of the asset being transferred.
    """
    
    def __init__(self, owner : str, buyer : str, asset_name : str, count : int) -> None:
        """
        The constructor for the Transaction class.
        
        Parameters:
            owner (str): The sender of the transaction.
            buyer (str): The receiver of the transaction.
            asset_name (str): The name of the asset being transferred.
            count (int): The quantity of the asset being transferred.
        """
        self.sender = owner
        self.buyer = buyer
        self.asset_name = asset_name
        self.count = count
        
    def __repr__(self) -> str:
        """
        Returns a string representation of the transaction.
        
        Returns:
            str: A formatted string describing the transaction.
        """
        return "({} -> {}) {} : {}".format(self.sender, self.buyer, self.asset_name, self.count)
    
    def __eq__(self, other) -> bool:
        """
        Checks if two transactions are equal.
        
        Parameters:
            other (Transaction): The transaction to compare against.
        
        Returns:
            bool: True if transactions are equal, False otherwise.
        """
        if isinstance(other, Transaction):
            return (self.sender == other.sender and 
                    self.buyer == other.buyer and 
                    self.asset_name == other.asset_name and 
                    self.count == other.count)
        return False
    
    def __hash__(self) -> int:
        """
        Computes the hash of the transaction.
        
        Returns:
            int: The hash value of the transaction.
        """
        return hash((self.sender, self.buyer, self.asset_name, self.count))

class Personal_asset:
    """
    This is a class representing a personal asset.
    
    Attributes:
        owner (str): The owner of the asset.
        asset_name (str): The name of the asset.
        count (int): The quantity of the asset.
    """
    
    def __init__(self, owner : str, asset_name : str, count : int) -> None:
        """
        The constructor for the Personal_asset class.
        
        Parameters:
            owner (str): The owner of the asset.
            asset_name (str): The name of the asset.
            count (int): The quantity of the asset.
        """
        self.owner = owner
        self.asset_name = asset_name
        self.count = count
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the personal asset.
        
        Returns:
            str: A formatted string describing the personal asset.
        """
        return "{} ({} : {})".format(self.owner, self.asset_name, self.count)
 
class Blockchain: 
    """
    This is a class representing a blockchain.
    
    Attributes:
        chain (list of Block): The list of blocks in the blockchain.
        public_ledger (dict): The public ledger recording asset ownership.
    """
    
    def __init__(self, difficulty=4) -> None:
        """
        The constructor for the Blockchain class.
        """
        self.chain = [self.create_genesis_block()]
        self.public_ledger: dict[str, dict[str, int]] = {}     
        self.difficulty = difficulty
    
    def create_genesis_block(self) -> Block:
        """
        Creates the first block in the blockchain.
        
        Returns:
            Block: The genesis block.
        """
        return Block(0, datetime.datetime.now(), "First Block", "0")
    
    def get_prevBlock(self) -> Block:
        """
        Retrieves the last block in the blockchain.
        
        Returns:
            Block: The last block in the blockchain.
        """
        return self.chain[-1]
   
    # creat a new block and and data to it 
    def add_Block(self, data) -> None:  
        """
        Adds a new block to the blockchain.
        
        Parameters:
            data (Transaction or Personal_asset): The data to be added to the new block.
        """
        self.update_public_ledger(data)
           
        new_block = Block(
            len(self.chain),
            datetime.datetime.now(),
            data,
            self.get_prevBlock().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def validate_transaction(self, transaction : Transaction) -> None:
        """
        Validates a transaction.
        
        Parameters:
            transaction (Transaction): The transaction to be validated.
        
        Raises:
            ValueError: If the transaction is invalid.
        """
        if transaction.sender not in self.public_ledger:
            raise ValueError("Sender not found")
        if transaction.buyer not in self.public_ledger:
            raise ValueError("Buyer not found")
        if transaction.asset_name not in self.public_ledger[transaction.sender]:
            raise ValueError(f"Sender don't have any {transaction.asset_name}")
        if transaction.count > self.public_ledger[transaction.sender][transaction.asset_name]:
            raise ValueError("Sender don't have enough")
    
    def update_public_ledger(self, data : Transaction | Personal_asset) -> None:
        """
        Updates the public ledger based on the provided data.
        
        Parameters:
            data (Transaction or Personal_asset): The data to update the ledger with.
        """
        if isinstance(data, Personal_asset):
            if data.owner in self.public_ledger:
                self.public_ledger[data.owner][data.asset_name] = data.count
            else:
                self.public_ledger[data.owner] = {data.asset_name: data.count}
        
        if isinstance(data, Transaction): 
            # Reduce asset count for the sender
            self.public_ledger[data.sender][data.asset_name] -= data.count
            if self.public_ledger[data.sender][data.asset_name] == 0:
                del self.public_ledger[data.sender][data.asset_name]
                
            # Increase asset count for the buyer
            self.public_ledger[data.buyer][data.asset_name] = self.public_ledger[data.buyer].get(data.asset_name, 0) + data.count
    
    def is_valid_chain(self) -> bool:
        """
        Checks if the blockchain is valid.
        
        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != previous_block.hash:
                return False

        return True


if __name__ == "__main__":
    # Backend testing
    
    blockchain = Blockchain()
    blockchain.add_Block(Personal_asset("Minh", "Ducati Super Car", 2))
    blockchain.add_Block(Personal_asset("Anonymous", "10$ USD", 100))
    blockchain.add_Block(Transaction("Minh", "Anonymous", "Ducati Super Car", 2))
    
        
    print("Is the blockchain valid?", blockchain.is_valid_chain())

    malicious_block = Block(len(blockchain.chain), datetime.datetime.now(), "Malicious data", blockchain.chain[-1].hash)
    malicious_block.hash = hashlib.sha256("fake_hash".encode('utf-8')).hexdigest()
    blockchain.chain.append(malicious_block)

    print("Is the blockchain valid?", blockchain.is_valid_chain())
    
    for block in blockchain.chain:
        print(block)
    
    print(json.dumps(blockchain.public_ledger, indent=2))