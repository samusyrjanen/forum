from db import db
import users

def thread_comments(id):#divide into smaller pieces?
    sql = 'select C.id, C.content, U.username, C.sent_at, count(L.comment_id) ' \
        'from comments C left join users U on C.user_id=U.id left join likes L ' \
        'on C.id=L.comment_id where C.thread_id=:id group by C.id, U.username order by C.id'
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