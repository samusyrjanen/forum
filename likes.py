from db import db
import users

def thread_likes(id):
    sql = 'select distinct user_id from likes where thread_id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def comment_likes(id):
    sql = 'select distinct U.username from likes L, users U ' \
        'where L.comment_id=:id and L.user_id=U.id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def send_like(thread_id, comment_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not comment_id:
        sql = 'insert into likes (user_id, thread_id) ' \
            'values (:user_id, :thread_id)'
        db.session.execute(sql, {'user_id':user_id, 'thread_id':thread_id})
        db.session.commit()
        return True
    else:
        sql = 'insert into likes (user_id, comment_id) ' \
            'values (:user_id, :comment_id)'
        db.session.execute(sql, {'user_id':user_id, 'comment_id':comment_id})
        db.session.commit()
        return True

def send_unlike(thread_id, comment_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not comment_id:
        sql = 'delete from likes where user_id=:user_id and thread_id=:thread_id'
        db.session.execute(sql, {'user_id':user_id, 'thread_id':thread_id})
        db.session.commit()
        return True
    else:
        sql = 'delete from likes where user_id=:user_id and comment_id=:comment_id'
        db.session.execute(sql, {'user_id':user_id, 'comment_id':comment_id})
        db.session.commit()
        return True