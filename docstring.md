# Class: Block

This is a class representing a single block in the blockchain.

**Attributes:**
- `index (int)`: The position of the block in the blockchain.
- `timestamp (datetime)`: The time at which the block was created.
- `data (any)`: The data stored in the block, typically a transaction or asset information.
- `prev_hash (str)`: The hash of the previous block in the blockchain.
- `hash (str)`: The hash of the current block.
- `nonce (int)`: The nonce used for the proof-of-work.

### Method: __init__

The constructor for the Block class.

**Parameters:**
- `index (int)`: The position of the block in the blockchain.
- `timestamp (datetime)`: The time at which the block was created.
- `data (any)`: The data stored in the block.
- `prev_hash (str)`: The hash of the previous block in the blockchain.
- `nonce (int)`: The nonce used for the proof-of-work.

### Method: calculate_hash

Computes the SHA-256 hash of the block's contents.

**Returns:**
- `str`: The computed hash as a hexadecimal string.

### Method: mine_block

Mines the block by finding a hash with a certain number of leading zeros.

**Parameters:**
- `difficulty (int)`: The number of leading zeros required in the hash.

### Method: __repr__

Returns a string representation of the block.

**Returns:**
- `str`: A formatted string describing the block.

# Class: Transaction

This is a class representing a transaction between two parties.

**Attributes:**
- `owner (str)`: The sender of the transaction.
- `buyer (str)`: The receiver of the transaction.
- `asset_name (str)`: The name of the asset being transferred.
- `count (int)`: The quantity of the asset being transferred.

### Method: __init__

The constructor for the Transaction class.

**Parameters:**
- `owner (str)`: The sender of the transaction.
- `buyer (str)`: The receiver of the transaction.
- `asset_name (str)`: The name of the asset being transferred.
- `count (int)`: The quantity of the asset being transferred.

### Method: __repr__

Returns a string representation of the transaction.

**Returns:**
- `str`: A formatted string describing the transaction.

### Method: __eq__

Checks if two transactions are equal.

**Parameters:**
- `other (Transaction)`: The transaction to compare against.

**Returns:**
- `bool`: True if transactions are equal, False otherwise.

### Method: __hash__

Computes the hash of the transaction.

**Returns:**
- `int`: The hash value of the transaction.

# Class: Personal_asset

This is a class representing a personal asset.

**Attributes:**
- `owner (str)`: The owner of the asset.
- `asset_name (str)`: The name of the asset.
- `count (int)`: The quantity of the asset.

### Method: __init__

The constructor for the Personal_asset class.

**Parameters:**
- `owner (str)`: The owner of the asset.
- `asset_name (str)`: The name of the asset.
- `count (int)`: The quantity of the asset.

### Method: __repr__

Returns a string representation of the personal asset.

**Returns:**
- `str`: A formatted string describing the personal asset.

# Class: Blockchain

This is a class representing a blockchain.

**Attributes:**
- `chain (list of Block)`: The list of blocks in the blockchain.
- `public_ledger (dict)`: The public ledger recording asset ownership.

### Method: __init__

The constructor for the Blockchain class.

### Method: create_genesis_block

Creates the first block in the blockchain.

**Returns:**
- `Block`: The genesis block.

### Method: get_prevBlock

Retrieves the last block in the blockchain.

**Returns:**
- `Block`: The last block in the blockchain.

### Method: add_Block

Adds a new block to the blockchain.

**Parameters:**
- `data (Transaction or Personal_asset)`: The data to be added to the new block.

### Method: validate_transaction

Validates a transaction.

**Parameters:**
- `transaction (Transaction)`: The transaction to be validated.

**Raises:**
- `ValueError`: If the transaction is invalid.

### Method: update_public_ledger

Updates the public ledger based on the provided data.

**Parameters:**
- `data (Transaction or Personal_asset)`: The data to update the ledger with.

### Method: is_valid_chain

Checks if the blockchain is valid.

**Returns:**
- `bool`: True if the blockchain is valid, False otherwise.
