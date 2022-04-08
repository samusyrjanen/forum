from db import db
from flask import session
import secrets
from werkzeug.security import check_password_hash, generate_password_hash

def user_id():
    return session.get('user_id', 0)

def login(username, password):
    sql = 'select id, password from users where username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['csrf_token'] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session['user_id']

def register(username, password):
    if len(username) < 3 or len(username) > 30 or len(password) < 3 or len(password) > 30:
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = 'insert into users (username, password) ' \
            'values (:username, :password)'
        db.session.execute(sql, {'username':username, 'password':hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def username():
    id = user_id()
    if id == 0:
        return None
    sql = 'select username from users where users.id=:id'
    result = db.session.execute(sql, {'id':id})
    username = result.fetchone()
    return username

def taken_usernames():
    sql = 'select username from users'
    result = db.session.execute(sql)
    return result.fetchall()

def get_user_id(username):
    sql = 'select id from users where username=:username'
    result = db.session.execute(sql, {'username':username})
    if result:
        return result.fetchone()[0]
    return 0

def get_all_users():
    sql = 'select id, username from users'
    result = db.session.execute(sql)
    return result.fetchall()

def search_users(username):
    sql = 'select id, username from users where username like :username order by username'
    result = db.session.execute(sql, {'username':'%'+username+'%'})
    return result.fetchall()