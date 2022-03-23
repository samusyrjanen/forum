from db import db
import users

def get_thread_list():
    sql = 'select T.content, U.username, T.sent_at from threads T, users U where T.user_id=U.id order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

