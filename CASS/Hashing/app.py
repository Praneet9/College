from flask import Flask, render_template, request, jsonify
import hashlib
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.cass
users = db.users

app = Flask(__name__)

def insert_data(args_dict):
    collection_name = users
    collection_name.insert_one(args_dict)
    print('Data inserted successfully')

def check(username, password):
    collection_name = users
    cols = collection_name.find({})
    for value in cols:
        if value['username'] == username and value['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest():
            return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user_login')
    password = request.form.get('password_login')
    hashed_password = hashlib.sha256(password.encode('utf-8'))
    if(check(username, password)):
        return "User authenticated!"
    else:
        return "Invalid Credentials"

@app.route('/register', methods=['POST', 'GET'])
def register():
    email = request.form.get('email_register')
    password = request.form.get('password_register')
    username = request.form.get('name')
    password = hashlib.sha256(password.encode('utf-8'))
    hashed_password = password.hexdigest()

    args = {'username': username, 'email': email, 'password': hashed_password}
    insert_data(args)

    return "User Registered"

if __name__ == '__main__':
    app.run(debug=True)