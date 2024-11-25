#!/usr/bin/env python3
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return ("Le bot est en ligne!")

def run():
    app.run(host="0.0.0.0", port=(5000))

def keep_alive():
    t = Thread(target=run)
    t.start()
