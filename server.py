# Opstarten met 
# gunicorn --bind 0.0.0.0:5000  wsgi:app

from flask import Flask, render_template, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies, set_refresh_cookies
)
import json
import database
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = True
jwt = JWTManager(app)

@app.route("/", methods=['get'])
def index():
  return render_template("index.html")


@app.route('/login', methods=['get'])
def login_form():
    return render_template('login_form.html')

@app.route('/login', methods=['post'])
def login():
    username = request.json.get('usr', None)
    password = request.json.get('pwd', None)
    access_token = create_access_token(identity=username) 
    refresh_token = create_refresh_token(identity=username)

    resp = jsonify({'login':True})
    set_access_cookies(resp, access_token) 
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@app.route('/test', methods=['get'])
@jwt_required
def test():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/timeline/<chapter>", methods=['get'])
def timeline(chapter):
    data = database.get_timeline(chapter)
    return jsonify(data) 

@app.route('/edit/<id>', methods=['get'])
@jwt_required
def edit(id):
    data = database.get_time_item(id)
    return render_template('form.html', result=data)

@app.route('/edit/<id>', methods=['put'])
@jwt_required
def update(id):
    print (request.json)
    n_id = database.update(request.json)
    return "{}".format(n_id), 200

@app.route('/position/<id>', methods=['put'])
@jwt_required
def update_position(id):
    database.update_position(id, request.json)


@app.route('/insert/', methods=['post'])
@jwt_required
def insert():
    id = database.insert(request.json) 
    reps = Response()
    resp.headers['Location'] = "http:/localhost/dreadnought/edit/{}".format(id)
    return resp, 201

@app.route('/del/<id>', methods=['delete'])
@jwt_required
def delete(id):
    database.delete(id)
    return "delete"



if __name__=='__main__':
    app.run(debug=True)
