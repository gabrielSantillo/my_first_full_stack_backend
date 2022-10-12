
from flask import Flask, request, make_response
import mariadb
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
from dbcreds import production_mode
import json

app = Flask(__name__)

@app.get('/api/candy')
def get_all_candys():
    results = run_statement('CALL get_all_candys()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occured.", default=str), 500)

@app.post('/api/candy')
def add_candy():
    is_valid = check_endpoint_info(request.json, ['name', 'image_url', 'description'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL insert_candy(?,?,?)',
    [request.json.get('name'), request.json.get('image_url'), request.json.get('description')])

    if(type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has ocurred.", default=str), 500)

@app.delete('/api/candy')
def delete_candy():
    invalid = check_endpoint_info(request.json, ['candy_id'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400) 

    results = run_statement('CALL delete_candy(?)',
    [request.json.get('candy_id')])

    if(type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    elif(results.startswith('Incorrect integer value')):
        return "This candy id doesn't exists. Please, insert an existing one."
    else:
        return make_response(json.dumps(results, default=str), 400)

if(production_mode):
    print("Running in Production Mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)