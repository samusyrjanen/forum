from db import db
import users

def thread_comments(id):
    sql = 'select C.id, C.content, U.username, C.sent_at ' \
        'from comments C, users U whith C.user_id=U.id ' \
        'and C.thread_id=:id order by C.id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()