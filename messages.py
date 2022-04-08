from db import db
import users

def received_messages(receiver_id):
    sql = 'select M.content, U.username, M.sent_at from messages M, users U ' \
        'where M.sender_id=U.id and M.receiver_id=:receiver_id order by M.id desc'
    result = db.session.execute(sql, {'receiver_id':receiver_id})
    return result.fetchall()

def sent_messages(sender_id):
    sql = 'select M.content, U.username, M.sent_at from messages M, users U ' \
        'where M.receiver_id=U.id and M.sender_id=:sender_id order by M.id desc'
    result = db.session.execute(sql, {'sender_id':sender_id})
    return result.fetchall()

def search_received_messages(receiver_id, content):
    sql = 'select M.content, U.username, M.sent_at from messages M, users U ' \
        'where M.sender_id=U.id and M.receiver_id=:receiver_id and ' \
        '(M.content like :content or U.username like :content) order by M.id desc'
    result = db.session.execute(sql, {'receiver_id':receiver_id, 'content':'%'+content+'%'})
    return result.fetchall()

def search_sent_messages(sender_id, content):
    sql = 'select M.content, U.username, M.sent_at from messages M, users U ' \
        'where M.receiver_id=U.id and M.sender_id=:sender_id and ' \
        '(M.content like :content or U.username like :content) order by M.id desc'
    result = db.session.execute(sql, {'sender_id':sender_id, 'content':'%'+content+'%'})
    return result.fetchall()

def send(content, receiver_username):
    sender_id = users.user_id()
    if sender_id == 0:
        return False
    receiver_id = users.get_user_id(receiver_username)
    if receiver_id == 0:
        return False
    sql = 'insert into messages (sender_id, receiver_id, content, sent_at) ' \
        'values (:sender_id, :receiver_id, :content, NOW())'
    db.session.execute(sql, {'sender_id':sender_id, 'receiver_id':receiver_id, 'content':content})
    db.session.commit()
    return True