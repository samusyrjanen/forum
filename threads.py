from db import db
import users

def get_thread_list():
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

def search_thread(topic):
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.topic like :topic order by T.id'
    result = db.session.execute(sql, {'topic':'%'+topic+'%'})
    return result.fetchall()

def get_specific_thread(id):
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def send(topic, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if len(content) < 1 or len(content) > 2000 or len(topic) < 1 or len(topic) > 200:
        return False
    sql = 'insert into threads (topic, content, user_id, sent_at) ' \
        'values (:topic, :content, :user_id, NOW())'
    db.session.execute(sql, {'topic':topic, 'content':content, 'user_id':user_id})
    db.session.commit()
    return True