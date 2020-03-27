import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class SuspectedCase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    device_mac_addr = db.Column(db.String(17), nullable = False)
    diagnosed_or_suspected = db.Column(db.Boolean(), nullable = False)

@app.route('/cases', methods=['GET', 'POST'])
def update_cases():
    if request.method == 'GET':
        # return list of all cases
        raw_cases = SuspectedCase.query.all()
        cases = list(map(lambda x : {
          'mac' : x.device_mac_addr,
          'diag_or_susp' : x.diagnosed_or_suspected}, raw_cases))
        return {'cases' : cases}
    elif request.method == 'POST':
        # create new case
        mac = request.form['mac']
        diag_or_susp = bool(request.form['diag_or_susp'])
        case_to_add = SuspectedCase(device_mac_addr = mac, diagnosed_or_suspected = diag_or_susp)
        db.session.add(case_to_add)
        db.session.commit()
        return {'msg' : 'created'}
