import hashlib
import json
import datetime 

class Block:   
    def __init__(self, index, timestamp, data, prev_hash) -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        hash_string = (str(self.index) + str(self.timestamp) + str(self.data) + self.prev_hash)
        return hashlib.sha256(hash_string.encode('utf-8')).hexdigest()
    
    def __repr__(self) -> str:
        StrBlock = f'''Block #{self.index} at {self.timestamp}
    Data: {self.data}
    Previous Hash: {self.prev_hash}
    Block Hash: {self.hash}
          '''
        return StrBlock
    
class Transaction: 
    def __init__(self, owner : str, buyer : str, asset_name : str, count : int) -> None:
        self.sender = owner
        self.buyer = buyer
        self.asset_name = asset_name
        self.count = count
        
    def __repr__(self) -> str:
        return "({} -> {}) {} : {}".format(self.sender, self.buyer, self.asset_name, self.count)

class Personal_asset:
    def __init__(self, owner : str, asset_name : str, count) -> None:
        self.owner = owner
        self.asset_name = asset_name
        self.count = count
    
    def __repr__(self) -> str:
        return "{} ({} : {})".format(self.owner, self.asset_name, self.count)
 
class Blockchain: 
    def __init__(self) -> None:
        self.chain = [self.creat_genesis_block()]
        self.public_ledger = {}          # record asset of all members

    # creat first block of blockchain
    def creat_genesis_block(self) -> Block:
        return Block(0, datetime.datetime.now(), "First Block", "0")
    
    def get_prevBlock(self) -> Block:
        return self.chain[-1]
   
    # creat a new block and and data to it 
    def add_Block(self, data) -> None:  
        self.update_public_ledger(data)
           
        new_block = Block(
            len(self.chain),
            datetime.datetime.now(),
            data,
            self.get_prevBlock().hash
        )
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        
    def update_public_ledger(self, data : Transaction | Personal_asset) -> None:
        if isinstance(data, Personal_asset):
            if data.owner in self.public_ledger:
                self.public_ledger[data.owner][data.asset_name] = data.count
            else:
                self.public_ledger[data.owner] = {data.asset_name: data.count}
        
        if isinstance(data, Transaction):
            if data.sender in self.public_ledger:
                if data.asset_name in self.public_ledger[data.sender]: 
                    if data.buyer in self.public_ledger:
                        # giảm số lượng tài sản bên nhận
                        if self.public_ledger[data.sender][data.asset_name] >= data.count:
                            self.public_ledger[data.sender][data.asset_name] -= data.count
                            if self.public_ledger[data.sender][data.asset_name] == 0:
                                del self.public_ledger[data.sender][data.asset_name]
                        else:
                            raise ValueError("Sender don't have enough")

                        # tăng số lượng tài sản bên nhận
                        if data.asset_name in self.public_ledger[data.buyer]:
                            self.public_ledger[data.buyer][data.asset_name] += data.count
                        else:
                            self.public_ledger[data.buyer][data.asset_name] = data.count
                    else:
                        raise ValueError("Buyer not found")
                else:
                    raise ValueError(f"Sender don't have any {data.asset_name}")
            else:
                raise ValueError("Sender not found")
    
    def is_valid_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != previous_block.hash:
                return False

        return True


if __name__ == "__main__":
    # Testing 
    
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