#!/usr/bin/env python2.7
# encoding: UTF-8

from flask import Flask
from flask import flash
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('base.html')

if __name__ == "__main__":
    app.run()
