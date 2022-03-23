from app import app
from flask import render_template, request, redirect
import threads

@app.route('/')
def index():
    list = threads.get_thread_list()
    return render_template('index.html', threads=list)