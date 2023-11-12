from db import db
from sqlalchemy.sql import text
import users

def get_list_with_answers_count():
    sql = text("SELECT M.id, M.topic, M.text, U.username, M.sent_at, COUNT(A.id) as answer_count "
               "FROM messages M "
               "JOIN users U ON M.user_id = U.id "
               "LEFT JOIN answers A ON M.id = A.message_id "
               "GROUP BY M.id, U.username ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic, texts):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if topic != "" and texts != "":
        sql = text("INSERT INTO messages (topic, text, user_id, sent_at) VALUES (:topic, :text, :user_id, NOW())")
        db.session.execute(sql, {"topic":topic, "text":texts, "user_id":user_id})
        db.session.commit()
        return True
    else:
        return False

def get_message(id):
    sql = text("SELECT M.id, M.topic, M.text, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id AND M.id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send_answer(answer_id, texts):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if texts != "":
        sql = text("INSERT INTO answers (message_id, answer, user_id, sent_at) VALUES (:message_id, :answer, :user_id, NOW())")
        db.session.execute(sql, {"message_id":answer_id, "answer":texts, "user_id":user_id})
        db.session.commit()
        return True
    else:
        return False


def get_answer(id):
    sql = text("SELECT A.answer, U.username, A.sent_at FROM answers A, users U WHERE A.user_id=U.id AND A.message_id=:id ORDER BY A.id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

