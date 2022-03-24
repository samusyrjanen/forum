from db import db
import users

def get_thread_list():
    sql = 'select T.content, U.username, T.sent_at, T.id from threads T, ' \
        'users U where T.user_id=U.id order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

def get_specific_thread(id):
    sql = 'select T.content, U.username, T.sent_at from threads T, ' \
        'users U where T.user_id=U.id and T.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()