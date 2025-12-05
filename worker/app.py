from flask import Flask
import requests
import os

app = Flask(__name__)

@app.route("/status")
def status():
    return {"worker":"running"}

@app.route("/process/<msg>")
def process(msg):
    print(f"[WORKER] Processing image: {msg}")
    return {"status":"processed","message":msg}

if __name__ =="__main__":
    app.run(host="0.0.0.0",port=5000)