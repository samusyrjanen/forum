from db import db
import users

def get_thread_list():
    sql = 'select T.id, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

def search_thread(content):
    sql = 'select T.id, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.content like :content order by T.id'
    result = db.session.execute(sql, {'content':'%'+content+'%'})
    return result.fetchall()

def get_specific_thread(id):
    sql = 'select T.id, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def send(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = 'insert into threads (content, user_id, sent_at) ' \
        'values (:content, :user_id, NOW())'
    db.session.execute(sql, {'content':content, 'user_id':user_id})
    db.session.commit()
    return True