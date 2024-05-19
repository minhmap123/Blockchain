from flask import Flask, render_template, request, redirect, url_for, flash, session
from blockchain import Block, Blockchain, Personal_asset, Transaction
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from os import path, getcwd

blockchain = Blockchain()
transaction_requests = {}

app = Flask(__name__)
app.secret_key = "Just_4_r@nd0m_k3y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
    @classmethod
    def populate_ledger(cls, ledger):
        users = cls.query.all()
        for user in users:
            ledger[user.username] = {}

@app.route('/login_register')
def login_register():
    return render_template('login_register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session["user"] = username
        flash('Login successful!', 'login_success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password. Please try again.', 'login_error')
        return redirect(url_for('login_register'))
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists. Please choose a different one.', 'register_error')
        return redirect(url_for('login_register'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists. Please choose a different one.', 'register_error')
        return redirect(url_for('login_register'))
    
    new_user = User(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now login.', 'register_success')
        return redirect(url_for('login_register'))
    except IntegrityError:
        db.session.rollback()
        flash('An error occurred during registration. Please try again.', 'register_error')
        return redirect(url_for('login_register'))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login_register'))

@app.route('/')
def index():
    if "user" in session:
        return render_template("index.html", blockchain= blockchain, transaction_requests= transaction_requests)
    else:
        return redirect(url_for('login_register'))

@app.route('/add_personal_asset', methods=['POST'])
def add_personal_asset():
    owner = session["user"]
    name = request.form['name']
    count = request.form['count']
    
    if not (name and count):
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

    if session["user"] != sender and session["user"] != buyer:
        flash('You are not authorized to perform this transaction.', 'add_transaction_error')
        return redirect(url_for('index'))

    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except ValueError:
        flash('Count must be a positive integer.', 'add_transaction_error')
        return redirect(url_for('index'))
    
    try:
        transaction = Transaction(sender, buyer, asset_name, count)
        
        if session["user"] == sender:
            receiver = buyer
        else:
            receiver = sender
        
        blockchain.validate_transaction(transaction)
        transaction_requests.setdefault(receiver, []).append(transaction)
        
        flash('Transaction request sent. Waiting for confirmation.', 'add_transaction_success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'add_transaction_error')
    
    return redirect(url_for('index'))

@app.route('/confirm_transaction', methods=['POST'])
def confirm_transaction():
    action = request.form['action']
    sender = request.form['sender']
    buyer = request.form['buyer']
    asset_name = request.form['asset_name']
    count = request.form['count']

    transaction = Transaction(sender, buyer, asset_name, int(count))

    if action == "confirm":
        blockchain.add_Block(transaction)
        flash('Transaction confirmed successfully!', 'confirm_transaction_success')
    elif action == "reject":
        flash('Transaction rejected.', 'reject_transaction_success')
        
    transaction_requests[session["user"]].remove(transaction)
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
    if not path.exists(path.join(getcwd(), "instance", "users.db")):
        with app.app_context():
            db.create_all()
        print("Created user database")
    else:
        with app.app_context():
            User.populate_ledger(blockchain.public_ledger)
            print("Loaded existing users into the public ledger")
    app.run(host="0.0.0.0", port=8080)