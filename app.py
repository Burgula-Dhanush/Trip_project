from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import subprocess
import os
from flask_pymongo import PyMongo
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tripdb'
mongo = PyMongo(app)

# Route to store user's geolocation in MongoDB
@app.route('/store_location', methods=['POST'])
def store_location():
    data = request.json
    username = data.get('username')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Update or insert location data in MongoDB
    mongo.db.users.update_one(
        {'username': username},
        {'$set': {'location': {'latitude': latitude, 'longitude': longitude}}},
        upsert=True
    )

    return jsonify({'status': 'success'})


# Route to retrieve user's geolocation from MongoDB
@app.route('/get_location/<user_id>', methods=['GET'])
def get_location(user_id):
    location_data = mongo.db.user_locations.find_one({'user_id': user_id}, {'_id': 0})
    return jsonify(location_data)

# Flag to check if Streamlit app is already running
streamlit_running = False

# @app.route('/')
# def index():
#     username = session.get('username')
#     return render_template('index1.html', username=username)

@app.route('/logout')
def logout():
    user_data_path = os.path.join(os.path.dirname(__file__), 'user_data.txt')

# Read data from the user_data file
    with open(user_data_path, "r") as file:
        data = file.readline().strip()

# Split the data into username and trips
    username, trips_data = map(str.strip, data.split(':'))

# Split trips_data into individual trips
    trips = [trip.strip() for trip in trips_data.split(',')]

# Find the document in MongoDB based on the username
    user_document = mongo.db.users.find_one({"username": username})

# If the document is found, update the 'trips' array
    if user_document:
        existing_trips = user_document.get("trips", [])
        
        if existing_trips:
            for trip in trips:
                if trip and trip not in existing_trips:  # Check if trip is not empty
                    existing_trips.append(trip)
        else:
        # If 'trips' array does not exist, create a new one
            existing_trips = [trip for trip in trips if trip]


        existing_trips = list(filter(None, existing_trips))

    # Update the document with the modified trips array
        mongo.db.users.update_one(
            {"_id": user_document["_id"]},
            {"$set": {"trips": existing_trips}}
        )
        print(f"Trips added to the user {username}: {trips}")

    session.pop('username', None)
    
    return redirect(url_for('index'))

@app.route('/store_address', methods=['POST'])
def store_address():
    data = request.json
    username = data.get('username')
    address = data.get('address')
    
    with open(os.path.join(os.path.dirname(__file__), 'streamlit', 'user_location.txt'), 'w', encoding='utf-8') as file:
          
          file.write(f"{username}, {address}")

    # Store address data in MongoDB
    mongo.db.users.update_one(
        {'username': username},
        {'$set': {'location.address': address}},
        upsert=True
    )

    return jsonify({'status': 'success'})

@app.route('/user/<username>')
def user_page(username):
    return render_template('index.html', username=username)

@app.route('/')
def index():
    if 'username' in session:

        username = session.get('username')
        trips_file_path = os.path.join(os.path.dirname(__file__), 'trips.txt')

    # Retrieve the trips from MongoDB
        trips = mongo.db.users.find_one({'username': username}, {'_id': 0, 'trips': 1})

        if trips and 'trips' in trips:
            trips_list = trips['trips']

        # Write the trips to the trips.txt file
            with open(trips_file_path, 'w') as file:
                file.write(', '.join(map(str, trips_list)))

        return render_template('index.html', username=session['username'])
    
    else:
    # If there is no username, empty the trips.txt file
        trips_file_path = os.path.join(os.path.dirname(__file__), 'trips.txt')
        with open(trips_file_path, 'w'):
            pass  # This creates an empty file
    
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        dob = request.json.get('dob')

        # Validate the form data if needed

        # Store user data in MongoDB
        mongo.db.users.insert_one({'username': username, 'password': password, 'dob': dob})

        return jsonify({'status':'success'})

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user_data = mongo.db.users.find_one({'username': username, 'password': password})

        if user_data:
            session['username'] = username  # Store username in session
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
    else:
        return render_template('login.html')
    

@app.route('/book')
def book():

        shared_data_path = os.path.join(os.path.dirname(__file__), 'user_data.txt')
        with open(shared_data_path, 'w') as file:
            file.write(f"{session.get('username')} : ")

        code_path = os.path.abspath("streamlit/code.py")
        
        subprocess.Popen(["streamlit", "run", code_path])

             
        return redirect(url_for('index'))
        

@app.route('/streamlit')
def streamlit():
    global streamlit_running

    if not streamlit_running and request.args.get('action') == 'plan_a_tour':
        code_path = os.path.abspath("streamlit/code.py")
        subprocess.Popen(["streamlit", "run", code_path])
        streamlit_running = True

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
