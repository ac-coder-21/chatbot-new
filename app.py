from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from chat import get_response
app = Flask(__name__)
CORS(app)

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    output = get_response(text)
    message = {"output": output}
    return jsonify(message)



if __name__ =="__main__":
    app.run(debug=True)