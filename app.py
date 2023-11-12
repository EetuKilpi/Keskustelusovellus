from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = text("SELECT id, topic, text, created_at FROM messages ORDER BY id DESC")
    result = db.session.execute(sql)
    messages = result.fetchall()
    return render_template("index.html", messages=messages)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    #if not user:
        # TODO: invalid username
    #else:
        #hash_value = user.password
        #if check_password_hash(hash_value, password):
            # TODO: correct username and password
        #else:
            # TODO: invalid password
    
    session["username"] = username
    return redirect("/")

@app.route("/createaccount",methods=["POST"])
def create_account():
    username = request.form["new_username"]
    password = request.form["new_password"]
    session["username"] = username
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    message = request.form["text"]
    if message != "":
        sql = text("INSERT INTO messages (topic, text, created_at) VALUES (:topic, :text, NOW())")
        db.session.execute(sql, {"topic":topic, "text":message})
    db.session.commit()
    return redirect("/")

@app.route("/message/<int:id>")
def message(id):
    sql = text("SELECT topic FROM messages WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("SELECT text FROM messages WHERE id=:id")
    sql2 = text("SELECT answer FROM answers WHERE message_id=:id")
    result = db.session.execute(sql, {"id":id})
    result2 = db.session.execute(sql2, {"id":id})
    texts = result.fetchone()[0]
    answers = result2.fetchall()
    return render_template("text.html", id=id, topic=topic, texts=texts, answers=answers)

@app.route("/answer", methods=["POST"])
def answer():
    answer_id = request.form["id"]
    texts = request.form["text"]
    if texts != "":
        sql = text("INSERT INTO answers (message_id, answer, sent_at) VALUES (:message_id, :answer,NOW())")
        db.session.execute(sql, {"message_id":answer_id, "answer":texts})
        db.session.commit()
    return redirect("/message/" + str(answer_id))

