from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from blockchain import Block, Blockchain, Personal_asset, Transaction

blockchain = Blockchain()

app = Flask(__name__)
app.secret_key = "Just_4_r@nd0m_k3y"

@app.route('/')
def index():
    return render_template("index.html", blockchain=blockchain)

@app.route('/add_personal_asset', methods=['POST'])
def add_personal_asset():
    owner = request.form['owner']
    name = request.form['name']
    count = request.form['count']
    
    if not (owner and name and count):
        flash('Please fill out all fields.', 'add_asset_error')
        return redirect(url_for('index'))
    
    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except ValueError:
        flash('Count must be a positive integer.', 'add_asset_error')
        return redirect(url_for('index'))
    
    try:
        blockchain.add_Block(Personal_asset(owner, name, count))
        flash('Personal asset added successfully!', 'add_asset_success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'add_asset_error')
        
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    buyer = request.form['buyer']
    asset_name = request.form['asset_name']
    count = request.form['transaction_count']
    
    if not (sender and buyer and asset_name and count):
        flash('Please fill out all fields.', 'add_transaction_error')
        return redirect(url_for('index'))

    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except ValueError:
        flash('Count must be a positive integer.', 'add_transaction_error')
        return redirect(url_for('index'))
    
    try:
        blockchain.add_Block(Transaction(sender, buyer, asset_name, count))
        flash('Transaction added successfully!', 'add_transaction_success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'add_transaction_error')
    
    return redirect(url_for('index'))

@app.route('/validate_blockchain')
def validate_blockchain():
    is_valid = blockchain.is_valid_chain()
    if is_valid:
        flash('Blockchain is valid!', 'valid_blockchain')
    else:
        flash('Blockchain is not valid!', 'invalid_blockchain')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='  0.0.0.0', port= 8080, debug= True)
    