from flask import Flask, request, make_response
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
from dbcreds import production_mode
import json

# calling the Flask function which will return a value that I will be used for my API
app = Flask(__name__)

# making a get request with the endpoint /api/candy


@app.get('/api/candy')
def get_all_candys():
    # calling the procedure
    results = run_statement('CALL get_all_candys()')

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not, sent back a message with the status code response
    if (type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occured.", default=str), 500)

# making a post request with the endpoint /api/candy


@app.post('/api/candy')
def add_candy():
    # calling the function that will verify the return value
    is_valid = check_endpoint_info(
        request.json, ['name', 'image_url', 'description'])
    # if the is_valid variable value is anything but None return with the make_response showing what was the error
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # calling the procedure
    results = run_statement('CALL insert_candy(?,?,?)',
                            [request.json.get('name'), request.json.get('image_url'), request.json.get('description')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not sent back a message with the status code response
    if (type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has ocurred.", default=str), 500)

# making a delete request with the endpoint /api/candy


@app.delete('/api/candy')
def delete_candy():
    # calling the function that will verify the return value
    is_valid = check_endpoint_info(request.json, ['candy_id'])
    # if the is_valid variable value is anything but None return with the make_response showing what was the error
    if (is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # calling the procedure
    results = run_statement('CALL delete_candy(?)',
                            [request.json.get('candy_id')])

    # checking to see if the response is a list and if yes, turn this response into a JSON and the status code response, if not sent back a message with the status code response
    if (type(results) == list):
        return make_response(json.dumps(results[0][0], default=str), 200)
    elif (results.startswith('Incorrect integer value')):
        return "This candy id doesn't exists. Please, insert an existing one."
    else:
        return make_response(json.dumps(results, default=str), 400)


# if statement to check if the production_mode variable is true, if yes, run in production mode, if not, run in testing mode
if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5134)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)
