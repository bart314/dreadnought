# Opstarten met 
# gunicorn --bind 0.0.0.0:5000  wsgi:app --error-logfile gunicorn.error.log --access-logfile gunicorn.log --capture-output

from flask import Flask, render_template, jsonify, request, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    get_raw_jwt
)
from datetime import timedelta
import json
import database

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600) 

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

#https://github.com/vimalloc/flask-jwt-extended/blob/bf1a521b444536a5baea086899636406122acbc5/examples/redis_blacklist.py#L59
@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = database.get_blacklist_token(jti)
    return entry['tot'] > 0


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
    if (username=='bart' and password=='dreadnought'):
        access_token = create_access_token(identity=username) 
        resp = jsonify({'login':True})
        set_access_cookies(resp, access_token) 
        return resp, 200
    else:
        return jsonify({'error':'incorrect credentials'}), 401


@app.route('/logout', methods=['get'])
@jwt_required
def logout():
    jwt = get_raw_jwt()['jti']
    database.blacklist_token(jwt)
    return jsonify({"msg": "Access token revoked"}), 200


@app.route('/test', methods=['get'])
@jwt_required
def test():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/chapters', methods=['get'])
def chapters():
    data = database.get_chapters();
    return jsonify(data)

@app.route('/chapter/<id>', methods=['get'])
def get_chapter(id):
    data = database.get_chapter_info(id)
    return jsonify(data)

@app.route("/timeline/<chapter>", methods=['get'])
def timeline(chapter):
    data = database.get_timeline(chapter)
    return jsonify(data) 

@app.route('/edit/<id>', methods=['get'])
@jwt_required
def edit(id):
    print (get_jwt_identity())
    data = database.get_time_item(id)
    return render_template('form.html', result=data)

@app.route('/edit/<id>', methods=['put'])
@jwt_required
def update(id):
    data = request.json 
    n_id = database.update(data)
    return "{}".format(n_id), 200

@app.route('/testput', methods=['put'])
@jwt_required
def testput():
    print (get_jwt_identity());
    return '  *** testput ***'

@app.route('/position/<id>', methods=['put'])
@jwt_required
def update_position(id):
    database.update_position(id, request.json)


@app.route('/insert/', methods=['post'])
@jwt_required
def insert():
    id = database.insert(request.json) 
    resp = Response()
    resp.headers['Location'] = "http:/localhost/dreadnought/edit/{}".format(id)
    return resp, 201

@app.route('/del/<id>', methods=['delete'])
@jwt_required
def delete(id):
    database.delete(id)
    return "delete"



if __name__=='__main__':
    app.run(debug=True)
