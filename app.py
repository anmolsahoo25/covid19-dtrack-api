import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import secrets
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
jwt = JWTManager(app)

class SuspectedCase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    device_bluetooth_id = db.Column(db.Binary, nullable = False)
    diagnosed_or_suspected = db.Column(db.Boolean(), nullable = False)

class DeviceBluetoothId(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    device_bluetooth_id = db.Column(db.Binary, nullable = False)

@app.route('/auth', methods=['POST'])
def auth():
    # implement phone auth

    # phone auth succesful, generate ID and check if
    new_id = secrets.token_bytes(8)
    while True:
        is_present = len(DeviceBluetoothId.query.filter_by
            (device_bluetooth_id = new_id).all()) != 0

        if is_present:
            new_id = secrets.token_bytes(8)
        else:
            break

    # insert into database
    db.session.add(DeviceBluetoothId(device_bluetooth_id = new_id))
    db.session.commit()

    # create access token
    expires = datetime.timedelta(days=180)
    access_token = create_access_token(
        identity = new_id.hex(), expires_delta = expires)

    # return the access token
    return jsonify(access_token=access_token, device_id=new_id.hex()), 200

@app.route('/cases', methods=['GET', 'POST'])
@jwt_required
def update_cases():
    if request.method == 'GET':
        # return list of all cases
        raw_cases = SuspectedCase.query.all()
        cases = list(map(lambda x : {
          'device_id' : x.device_bluetooth_id.hex(),
          'diag_or_susp' : x.diagnosed_or_suspected}, raw_cases))
        return {'cases' : cases}
    elif request.method == 'POST':
        # # create new case
        # device_id = bytes.fromhex(request.form['device_id'])
        # diag_or_susp = bool(request.form['diag_or_susp'])
        # case_to_add = SuspectedCase(device_bluetooth_id = device_id, diagnosed_or_suspected = diag_or_susp)
        # db.session.add(case_to_add)
        # db.session.commit()
        # return {'msg' : 'created'}
        return jsonify({'msg' : 'Needs admin access'}), 401
