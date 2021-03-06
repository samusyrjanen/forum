from db import db
import users

def get_thread_list_new():
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'group by T.id, U.username order by T.id desc'
    result = db.session.execute(sql)
    return result.fetchall()

def get_thread_list_old():
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'group by T.id, U.username order by T.id'
    result = db.session.execute(sql)
    return result.fetchall()

def get_thread_list_liked():
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'group by T.id, U.username order by lamount desc'
    result = db.session.execute(sql)
    return result.fetchall()

def search_thread(topic):
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'where (T.topic like :topic or U.username like :topic) group by T.id, U.username order by T.id desc'
    result = db.session.execute(sql, {'topic':'%'+topic+'%'})
    return result.fetchall()

def search_thread_old(topic):
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'where (T.topic like :topic or U.username like :topic) group by T.id, U.username order by T.id'
    result = db.session.execute(sql, {'topic':'%'+topic+'%'})
    return result.fetchall()

def search_thread_liked(topic):
    sql = 'select T.id, T.topic, T.content, U.username, T.sent_at, count(L.id) as lamount ' \
        'from threads T left join users U on T.user_id=U.id left join likes L on L.thread_id=T.id ' \
        'where (T.topic like :topic or U.username like :topic) group by T.id, U.username order by lamount desc'
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

def delete(id):
    if not get_specific_thread(id):
        return False
    sql = 'delete from threads where id=:id'
    db.session.execute(sql, {'id':id})
    db.session.commit()
    return True

def user_id(thread_id):
    sql = 'select U.id from threads T, users U where T.user_id=U.id and T.id=:thread_id'
    result = db.session.execute(sql, {'thread_id':thread_id})
    return result.fetchone()[0]