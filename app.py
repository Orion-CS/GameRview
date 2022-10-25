# GameRview Semester Project

from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash

# make sure the script's directory is in Python's import path
# this is only required when run from a different directory
import os, sys
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'spiderweb'

@app.route('/')
def index():
    return "GameRview"