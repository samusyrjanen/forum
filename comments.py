from db import db
import users

def thread_comments(id):
    sql = 'select C.id, C.content, U.username, C.sent_at ' \
        'from comments C, users U where C.user_id=U.id ' \
        'and C.thread_id=:id order by C.id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def send(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = 'insert into comments (content, user_id, sent_at, thread_id) ' \
        'values (:content, :user_id, NOW(), :thread_id)'
    db.session.execute(sql, {'content':content, 'user_id':user_id, 'thread_id':thread_id})
    db.session.commit()
    return True