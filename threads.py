from db import db
import users

def get_thread_list():
    sql = 'select T.id, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

def get_specific_thread(id):
    sql = 'select T.id, T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def send(content):
    sql = 'insert into threads (content, user_id) ' \
        'values (:content, 1)'
    db.session.execute(sql, {'content':content})
    db.session.commit()
    return True