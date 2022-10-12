
from flask import Flask, request, make_response
from dbhelpers import run_statement
from apihelpers import check_endpoint_info
from dbcreds import production_mode
import json

app = Flask(__name__)



if(production_mode):
    print("Running in Production Mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)