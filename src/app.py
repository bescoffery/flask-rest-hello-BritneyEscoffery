"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Event
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    users = User.query.all()
    users_list = [item.serialize() for item in users]
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "data": users_list
    }

    return jsonify(response_body), 200

@app.route('/event', methods=['GET'])
def event_column():
    all_events = Event.query.all()
    event_list = [item.serialize() for item in all_events]
    
    return jsonify (event_list), 200

@app.route('/event', methods=['POST'])
def event_add():
    body = request.get_json()
    name_data = body['name']
    event_planner_data = body['event_planner']
    new_event = Event(
        name = name_data, 
        event_planner = event_planner_data
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.serialize()), 200

@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    body = request.get_json()
    event = db.session.get(Event, event_id)
    if event: 

        print ("event tag!!!!!!:",event)
        event.name = body["name"]
        db.session.commit()

        return jsonify(event.serialize()), 200
    else:
        return "no event with that id!!!!"

@app.route('/event/<int:event_id>', methods=['DELETE'])
def event_delete(event_id):
    event = db.session.get(Event, event_id)
    db.session.add(event)
    db.session.commit()
    
    return jsonify(event.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
