from flask import Flask, request, jsonify
from flask_cors import CORS
import  ApiTwee
app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json  # React-la send pannina JSON data
    print("Received:", data)

    response = {"message": "Data received successfully!", "yourData": data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
