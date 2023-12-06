from db import db
from sqlalchemy.sql import text
import users

def get_list():
    sql = text("SELECT M.id, M.topic, M.text, M.user_id, U.username, M.sent_at, COUNT(A.id) as answer_count, M.edited, M.private "
               "FROM messages M "
               "JOIN users U ON M.user_id = U.id "
               "LEFT JOIN answers A ON M.id = A.message_id "
               "GROUP BY M.id, U.username ORDER BY M.id DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic, texts, privacy):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if topic != "" and texts != "":
        sql = text("INSERT INTO messages (topic, text, user_id, sent_at, private) VALUES (:topic, :text, :user_id, NOW(), :private)")
        db.session.execute(sql, {"topic":topic, "text":texts, "user_id":user_id, "private":privacy})        
        db.session.commit()
        return True
    else:
        return False

def get_message(id):
    sql = text("SELECT M.id, M.topic, M.text, M.user_id, U.username, M.sent_at, M.edited, M.private FROM messages M, users U WHERE M.user_id=U.id AND M.id=:id")
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
    sql = text("SELECT A.id, A.answer, A.user_id, U.username, A.sent_at, A.edited FROM answers A, users U WHERE A.user_id=U.id AND A.message_id=:id ORDER BY A.id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def search(query):
    sql = text("SELECT M.id, M.topic, M.text, M.user_id, U.username, M.sent_at, COUNT(A.id) as answer_count, M.edited, M.private "
               "FROM messages M "
               "JOIN users U ON M.user_id = U.id "
               "LEFT JOIN answers A ON M.id = A.message_id "
               "WHERE lower(topic) LIKE lower(:query) "
               "GROUP BY M.id, U.username ORDER BY M.id")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    return result.fetchall()

def delete_answer(answer_id):
    sql_delete = text("DELETE FROM answers WHERE id = :answer_id")
    db.session.execute(sql_delete, {"answer_id": answer_id})
    db.session.commit()
    return True

def delete_message(message_id):
    sql_delete = text("DELETE FROM messages WHERE id = :message_id")
    db.session.execute(sql_delete, {"message_id": message_id})
    db.session.commit()
    return True

def allow_user(user_id, id, message_or_answer_or_poll):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if message_or_answer_or_poll == 0:
        sql = text("SELECT user_id FROM messages WHERE id = :message_id")
        result = db.session.execute(sql, {"message_id": id})
    elif message_or_answer_or_poll == 1:
        sql = text("SELECT user_id FROM answers WHERE id = :answer_id")
        result = db.session.execute(sql, {"answer_id": id})
    elif message_or_answer_or_poll == 2:
        sql = text("SELECT user_id FROM polls WHERE id = :poll_id")
        result = db.session.execute(sql, {"poll_id": id})
    allowed_user_id = result.scalar()
    if allowed_user_id == user_id:
        return True
    else:
        return False

def edit_answer(answer_id):
    sql = text("SELECT * FROM answers WHERE id = :answer_id")
    result = db.session.execute(sql, {"answer_id": answer_id})
    return result.fetchone()

def update_answer(answer_id, new_text):
    sql_update = text("UPDATE answers SET answer = :new_text, sent_at = NOW(), edited = TRUE WHERE id = :answer_id")
    db.session.execute(sql_update, {"new_text": new_text, "answer_id": answer_id})
    db.session.commit()
    return True

def edit_message(message_id):
    sql = text("SELECT * FROM messages WHERE id = :message_id")
    result = db.session.execute(sql, {"message_id": message_id})
    return result.fetchone()

def update_message(message_id, new_topic, new_text):
    sql_update = text("UPDATE messages SET topic = :new_topic, text = :new_text, sent_at = NOW(), edited = TRUE WHERE id = :message_id")
    db.session.execute(sql_update, {"new_topic": new_topic, "new_text": new_text, "message_id": message_id})
    db.session.commit()
    return True

def add_favorite(message_id, user_id):
    try:
        sql = text("INSERT INTO favorites (message_id, user_id) VALUES (:message_id, :user_id)")
        db.session.execute(sql, {"message_id": message_id, "user_id": user_id})        
        db.session.commit()
    except:
        return False
    return True

def get_favorite_messages(user_id):
    sql = text("SELECT M.id, M.topic, M.text, M.user_id, U.username, M.sent_at, COUNT(A.id) as answer_count, M.edited, M.private "
               "FROM messages M "
               "JOIN users U ON M.user_id = U.id "
               "LEFT JOIN answers A ON M.id = A.message_id "
               "JOIN favorites F ON M.id = F.message_id "
               "WHERE F.user_id = :user_id "
               "GROUP BY M.id, U.username ORDER BY M.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def get_favorite_message_ids(user_id):
    sql = text("SELECT M.id "
               "FROM messages M "
               "JOIN favorites F ON M.id = F.message_id "
               "WHERE F.user_id = :user_id ")
    result = db.session.execute(sql, {"user_id": user_id})
    return [record[0] for record in result.fetchall()]


def remove_favorite(message_id, user_id):
    sql_delete = text("DELETE FROM favorites WHERE message_id = :message_id AND user_id = :user_id")
    db.session.execute(sql_delete, {"message_id": message_id, "user_id": user_id})
    db.session.commit()
    return True


def get_polls():
    sql = text("SELECT P.id, P.topic, P.user_id, U.username, P.created_at "
               "FROM polls P "
               "JOIN users U ON P.user_id = U.id "
               "GROUP BY P.id, U.username ORDER BY P.id DESC")
    result = db.session.execute(sql)
    return result.fetchall()

def create_poll(topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if topic != "":
        sql = text("INSERT INTO polls (topic, user_id, created_at) VALUES (:topic, :user_id, NOW()) RETURNING id")
        result = db.session.execute(sql, {"topic":topic, "user_id":user_id})
        return result.fetchone()[0]
    else:
        return False
    
def create_choices(poll_id, choices):
    for choice in choices:
        if choice != "":
            sql = text("INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)")
            db.session.execute(sql, {"poll_id":poll_id, "choice":choice})
    db.session.commit()
    return True

def get_poll_topic(id):
    sql = text("SELECT topic FROM polls WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_poll_choices(id):
    sql = text("SELECT id, choice FROM choices WHERE poll_id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def poll_answer(choice_id):
    sql = text("INSERT INTO poll_answers (choice_id, sent_at) VALUES (:choice_id, NOW())")
    db.session.execute(sql, {"choice_id":choice_id})
    db.session.commit()
    return True

def get_poll_results(id):
    sql = text("SELECT c.choice, COUNT(a.id) FROM choices c LEFT JOIN poll_answers a "
               "ON c.id=a.choice_id WHERE c.poll_id=:poll_id GROUP BY c.id")
    result = db.session.execute(sql, {"poll_id":id})
    return result.fetchall()

def get_last_poll_answer(poll_id):
    sql = text("SELECT MAX(sent_at) FROM poll_answers WHERE choice_id IN (SELECT id FROM choices WHERE poll_id=:poll_id)")
    result = db.session.execute(sql, {"poll_id": poll_id})
    return result.scalar()

def delete_poll(poll_id):
    sql_delete = text("DELETE FROM polls WHERE id = :poll_id")
    db.session.execute(sql_delete, {"poll_id": poll_id})
    db.session.commit()
    return True
