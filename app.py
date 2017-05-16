from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from keras.models import load_model
from keras.preprocessing import sequence
from database import db
from models import Name

import json
import numpy as np
import re
import string
import yaml

config = yaml.load(open('config.yaml'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
app.secret_key = config['SECRET_KEY']
db.init_app(app)
model = None

@app.route('/api', methods=['GET'])
def index():
    if request.method == 'GET':
        if not request.args.getlist('name'):
            return json.dumps({'status': 'error', 'message': 'Please input a name!'})
        else:
            names = request.args.getlist('name')
            proba = infer(names)
            gender = np.where(proba > .5, 'male', 'female').reshape(-1).tolist()
            proba = change_proba(proba).reshape(-1).tolist()
            if len(names) == 1:
                values = json.dumps({'name': names[0], 'gender': gender[0], 'probability': proba[0]})
            else:
                values = json.dumps({'name': names, 'gender': gender, 'probability': proba})
            return values

def clean_name(name):
    alphanum_pattern = re.compile('([^\s\w])+')
    return alphanum_pattern.sub('', name)

def name_to_tensor(line):
    letters = " " + string.lowercase
    n_letters = len(letters)
    return [letters.find(letter) for letter in clean_name(line)]

def padding(tensor):
    maxlen = 48
    return sequence.pad_sequences(tensor, maxlen=maxlen)

def import_model():
    global model
    model = load_model(config['MODEL_FILE'])

def infer(names):
    global model

    if model == None:
        import_model()

    tensor = [name_to_tensor(name.lower()) for name in names]
    X = padding(tensor)
    return model.predict(X)

def change_proba(proba):
    if proba < .5:
        proba = 1 - proba
    return round(proba * 100, 2)

change_proba = np.vectorize(change_proba)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')