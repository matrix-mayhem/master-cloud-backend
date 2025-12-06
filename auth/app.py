from flask import Flask, request, jsonify
import jwt
from datetime import datetime
import os

app = Flask(__name__)

@app.post("/login")
def login():
    data = request.get_json()
    token = jwt.encode(
        {"user":data["username"], 
         "exp":datetime.utcnow()+datetime.timedelta(hours=1)},
         os.getenv("SECRET_FLASK"),
         algorithm=os.getenv("ALGORITHM")
    )
    return jsonify({"token":token})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)