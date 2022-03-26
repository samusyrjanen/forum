from app import app
from flask import render_template, request, redirect, session
import threads, comments, users, likes

@app.route('/')
def index():
    username = users.username()
    list = threads.get_thread_list()
    return render_template('index.html', username=username, threads=list)

@app.route('/result')
def result():
    query = request.args['query']
    if not query:
        return redirect('/')
    username = users.username()
    list = threads.search_thread(query)
    return render_template('index.html', username=username, threads=list)

@app.route('/thread/<int:id>')
def thread(id):
    thread = threads.get_specific_thread(id)
    comment_list = comments.thread_comments(id)
    thread_like_list = [i[0] for i in likes.thread_likes(id)]
    user_id = users.user_id()
    username = users.username()
    return render_template('thread.html', thread=thread,
        comment_list=comment_list, count_thread_likes=len(thread_like_list),
        user_id=user_id, thread_likes=thread_like_list, username=username)#variables?

@app.route('/create_thread')
def create_thread():
    return render_template('create_thread.html')

@app.route('/send_thread', methods=['POST'])
def send_thread():
    content = request.form['content']
    if session['csrf_token'] == request.form['csrf_token']:
        if threads.send(content):
            return redirect('/')
    else:
        return render_template('/error.html', message="Couldn't create thread, make sure you're logged in")

@app.route('/comment/<int:id>')
def comment(id):
    thread = threads.get_specific_thread(id)
    return render_template('comment.html', thread=thread)

@app.route('/send_comment', methods=['POST'])
def send_comment():
    thread_id = request.form['id']
    content = request.form['content']
    if session['csrf_token'] == request.form['csrf_token']:
        if comments.send(content, thread_id):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't send comment, make sure you're logged in")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':#what does this do?
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
        else:
            return render_template('/error.html', message="Couldn't login, check username and password")

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
        else:
            return render_template('/error.html', message="Couldn't register, check username and password")

@app.route('/send_thread_like', methods=['POST'])
def send_thread_like():
    thread_id = request.form['id']
    if session['csrf_token'] == request.form['csrf_token']:
        if likes.send_like(thread_id, None):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't send like, make sure you're logged in")

@app.route('/send_thread_unlike', methods=['POST'])
def send_thread_unlike():
    thread_id = request.form['id']
    if session['csrf_token'] == request.form['csrf_token']:
        if likes.send_unlike(thread_id, None):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't send unlike, make sure you're logged in")