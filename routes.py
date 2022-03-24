from app import app
from flask import render_template, request, redirect
import threads
import comments

@app.route('/')
def index():
    list = threads.get_thread_list()
    return render_template('index.html', threads=list)

@app.route('/thread/<int:id>')
def thread(id):
    thread = threads.get_specific_thread(id)
    comment_list = comments.thread_comments(id)
    return render_template('thread.html', thread=thread, comment_list=comment_list)

@app.route('/create_thread')
def create_thread():
    return render_template('create_thread.html')