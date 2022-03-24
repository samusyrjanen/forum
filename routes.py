from app import app
from flask import render_template, request, redirect
import threads

@app.route('/')
def index():
    list = threads.get_thread_list()
    return render_template('index.html', threads=list)

@app.route('/thread/<int:id>')
def thread(id):
    thread = threads.get_specific_thread(id)
    return render_template('thread.html', thread=thread)