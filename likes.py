from db import db
import users

def thread_likes(id):
    sql = 'select distinct user_id from likes where thread_id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def comment_likes(id):
    sql = 'select distinct user_id from likes where comment_id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def send_like(thread_id, comment_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if not comment_id:
        likes = [i[0] for i in thread_likes(thread_id)]
        if user_id in likes:
            return True
        sql = 'insert into likes (user_id, thread_id) ' \
            'values (:user_id, :thread_id)'
        db.session.execute(sql, {'user_id':user_id, 'thread_id':thread_id})
        db.session.commit()
        return True
    else:
        likes = [i[0] for i in comment_likes(comment_id)]
        if user_id in likes:
            return True
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
        likes = [i[0] for i in thread_likes(thread_id)]
        if user_id not in likes:
            return True
        sql = 'delete from likes where user_id=:user_id and thread_id=:thread_id'
        db.session.execute(sql, {'user_id':user_id, 'thread_id':thread_id})
        db.session.commit()
        return True
    else:
        likes = [i[0] for i in comment_likes(comment_id)]
        if user_id not in likes:
            return True
        sql = 'delete from likes where user_id=:user_id and comment_id=:comment_id'
        db.session.execute(sql, {'user_id':user_id, 'comment_id':comment_id})
        db.session.commit()
        return True