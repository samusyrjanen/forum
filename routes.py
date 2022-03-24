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

@app.route('/send_thread', methods=['POST'])
def send_thread():
    content = request.form['content']
    if threads.send(content):
        return redirect('/')

@app.route('/comment/<int:id>')
def comment(id):
    thread = threads.get_specific_thread(id)
    return render_template('comment.html', thread=thread)

@app.route('/send_comment', methods=['POST'])
def send_comment():
    thread_id = request.form['id']
    content = request.form['commentcontent']##########
    if comments.send(content, thread_id):
        return redirect('/thread/' + str(thread_id))