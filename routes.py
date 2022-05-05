from app import app
from flask import render_template, request, redirect, session
import threads, comments, users, likes, messages

@app.route('/')
def index():
    username = users.username()
    list = threads.get_thread_list_new()
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, admin_value=admin_value)

@app.route('/old')
def old():
    username = users.username()
    list = threads.get_thread_list_old()
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, admin_value=admin_value)

@app.route('/liked')
def liked():
    username = users.username()
    list = threads.get_thread_list_liked()
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, admin_value=admin_value)

@app.route('/result')
def result():
    query = request.args['query']
    if not query:
        return redirect('/')
    username = users.username()
    list = threads.search_thread(query)
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, query=query, admin_value=admin_value)

@app.route('/result/old')
def result_old():
    query = request.args['query']
    if not query:
        return redirect('/')
    username = users.username()
    list = threads.search_thread_old(query)
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, query=query, admin_value=admin_value)

@app.route('/result/liked')
def result_liked():
    query = request.args['query']
    if not query:
        return redirect('/')
    username = users.username()
    list = threads.search_thread_liked(query)
    admin_value = users.admin_value()
    return render_template('index.html', username=username, threads=list, query=query, admin_value=admin_value)

@app.route('/thread/<int:id>')
def thread(id):
    thread = threads.get_specific_thread(id)
    comment_list = comments.thread_comments(id)
    thread_like_list = [i[0] for i in likes.thread_likes(id)]
    user_id = users.user_id()
    username = users.username()
    admin_value = users.admin_value()
    return render_template('thread.html', thread=thread,
        comment_list=comment_list, count_thread_likes=len(thread_like_list),
        user_id=user_id, thread_likes=thread_like_list, username=username,
        admin_value = admin_value)

@app.route('/thread/<int:id>/old')
def thread_old(id):
    thread = threads.get_specific_thread(id)
    comment_list = comments.thread_comments_old(id)
    thread_like_list = [i[0] for i in likes.thread_likes(id)]
    user_id = users.user_id()
    username = users.username()
    admin_value = users.admin_value()
    return render_template('thread.html', thread=thread,
        comment_list=comment_list, count_thread_likes=len(thread_like_list),
        user_id=user_id, thread_likes=thread_like_list, username=username,
        admin_value = admin_value)
    
@app.route('/thread/<int:id>/liked')
def thread_liked(id):
    thread = threads.get_specific_thread(id)
    comment_list = comments.thread_comments_liked(id)
    thread_like_list = [i[0] for i in likes.thread_likes(id)]
    user_id = users.user_id()
    username = users.username()
    admin_value = users.admin_value()
    return render_template('thread.html', thread=thread,
        comment_list=comment_list, count_thread_likes=len(thread_like_list),
        user_id=user_id, thread_likes=thread_like_list, username=username,
        admin_value = admin_value)

@app.route('/create_thread')
def create_thread():
    username = users.username()
    admin_value = users.admin_value()
    return render_template('create_thread.html', username=username, admin_value=admin_value)

@app.route('/send_thread', methods=['POST'])
def send_thread():
    topic = request.form['topic']
    content = request.form['content']
    if session['csrf_token'] == request.form['csrf_token']:
        if threads.send(topic, content):
            return redirect('/')
    return render_template('/error.html', message="Couldn't create thread, make sure you're logged in")

@app.route('/comment/<int:id>')
def comment(id):
    thread = threads.get_specific_thread(id)
    username = users.username()
    admin_value = users.admin_value()
    return render_template('comment.html', thread=thread, username=username, admin_value=admin_value)

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
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
        else:
            return render_template('/login.html', message="Couldn't login, wrong username or password")

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
        message = ''
        if username in [i[0] for i in users.taken_usernames()]:
            message += 'That username is already taken. '
        if password1 != password2:
            message += 'Passwords were different.'
        if message:
            return render_template('register.html', message=message)
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

@app.route('/send_comment_like', methods=['POST'])
def send_comment_like():
    comment_id = request.form['comment_id']
    thread_id = request.form['thread_id']
    if session['csrf_token'] == request.form['csrf_token']:
        if likes.send_like(None, comment_id):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't send like, make sure you're logged in")

@app.route('/send_comment_unlike', methods=['POST'])
def send_comment_unlike():
    comment_id = request.form['comment_id']
    thread_id = request.form['thread_id']
    if session['csrf_token'] == request.form['csrf_token']:
        if likes.send_unlike(None, comment_id):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't send unlike, make sure you're logged in")

@app.route('/message/<username>')
def message(username):############################################
    admin_value = users.admin_value()
    return render_template('send_message.html', username=username, admin_value=admin_value)

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.form['content']
    username = request.form['username']
    if session['csrf_token'] == request.form['csrf_token']:
        if messages.send(content, username):
            return redirect('/messages')
    return render_template('/error.html', message="Couldn't send message, make sure you're logged in")

@app.route('/users')
def users_page():
    user_list = users.get_all_users()
    user_id = users.user_id()
    username = users.username()
    admin_value = users.admin_value()
    if user_id == 0:
        return render_template('users.html', users=user_list, username=username, admin_value=admin_value)
    return render_template('users.html', users=user_list, user_id=user_id, username=username, admin_value=admin_value)

@app.route('/users/result')
def users_search():
    query = request.args['query']
    user_id = users.user_id()
    username = users.username()
    admin_value = users.admin_value()
    if not query:
        user_list = users.get_all_users()
        return render_template('users.html', users=user_list, user_id=user_id, username=username, admin_value=admin_value)
    user_list = users.search_users(query)
    return render_template('users.html', users=user_list, query=query, user_id=user_id, username=username, admin_value=admin_value)

@app.route('/messages')
def messages_page():
    user_id = users.user_id()
    message_list = messages.received_messages(user_id)
    username = users.username()
    admin_value = users.admin_value()
    return render_template('messages.html', messages=message_list, username=username, admin_value=admin_value)

@app.route('/messages/result')
def messages_search():
    user_id = users.user_id()
    query = request.args['query']
    username = users.username()
    admin_value = users.admin_value()
    if not query:
        return redirect('/messages')
    message_list = messages.search_received_messages(user_id, query)
    return render_template('messages.html', messages=message_list, query=query, username=username, admin_value=admin_value)

@app.route('/sent_messages')
def sent_messages():
    user_id = users.user_id()
    message_list = messages.sent_messages(user_id)
    username = users.username()
    admin_value = users.admin_value()
    return render_template('sent_messages.html', messages=message_list, username=username, admin_value=admin_value)

@app.route('/sent_messages/result')
def sent_messages_search():
    user_id = users.user_id()
    query = request.args['query']
    username = users.username()
    admin_value = users.admin_value()
    if not query:
        return redirect('/sent_messages')
    message_list = messages.search_sent_messages(user_id, query)
    return render_template('sent_messages.html', messages=message_list, query=query, username=username, admin_value=admin_value)

@app.route('/delete_thread', methods=['POST'])
def delete_thread():
    thread_id = request.form['thread_id']
    thread_user_id = threads.user_id(thread_id)
    user_id = users.user_id()
    admin_value = users.admin_value()
    if thread_user_id != user_id and admin_value != 1:
        return render_template('/error.html', message="Couldn't delete thread")
    if request.form['csrf_token'] == session['csrf_token']:
        if threads.delete(thread_id):
            return redirect('/')
    return render_template('/error.html', message="Couldn't delete thread")

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    comment_id = request.form['comment_id']
    comment = comments.get_specific_comment(comment_id)
    user_id = users.user_id()
    admin_value = users.admin_value()
    thread_id = request.form['thread_id']
    if comment.user_id != user_id and admin_value != 1:
        return render_template('/error.html', message="Couldn't delete thread")
    if request.form['csrf_token'] == session['csrf_token']:
        if comments.delete(comment_id):
            return redirect('/thread/' + str(thread_id))
    return render_template('/error.html', message="Couldn't delete thread")