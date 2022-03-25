from app import app
from flask import render_template, request, redirect
import threads, comments, users

@app.route('/')
def index():
    user_id = users.user_id()
    list = threads.get_thread_list()
    return render_template('index.html', user_id=user_id, threads=list)

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
    content = request.form['content']
    if comments.send(content, thread_id):
        return redirect('/thread/' + str(thread_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':#what does this do?
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if users.register(username, password1):
            return redirect('/')