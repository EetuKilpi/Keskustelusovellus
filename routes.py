from app import app
from flask import render_template, request, redirect, url_for
import messages, users


@app.route("/")
def index():
    messages_with_count = messages.get_list_with_answers_count()
    return render_template("index.html", messages=messages_with_count)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    topic = request.form["topic"]
    text = request.form["text"]
    if messages.send(topic, text):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys epäonnistui",url="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana",url="login")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat",url="register")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut",url="register")

@app.route("/message/<int:id>")
def message(id):
    list = messages.get_message(id)
    list2 = messages.get_answer(id)
    return render_template("text.html", message=list, answers=list2)

@app.route("/answer", methods=["POST"])
def answer():
    answer_id = request.form["id"]
    texts = request.form["text"]
    if messages.send_answer(answer_id, texts):
        return redirect("/message/" + str(answer_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut", url="message/"+str(answer_id))

@app.route("/result")
def result():
    query = request.args["query"]
    if query != "":
        message = messages.search(query)
    return render_template("result.html", messages=message ,query=query)

@app.route("/delete_answer", methods=["POST"])
def delete_answer():
    answer_id = request.form["answer_id"]
    message_id = request.form["message_id"]
    if messages.delete_answer(answer_id):
        return redirect("/message/" + str(message_id))
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="message/"+str(answer_id))

@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_id = request.form["message_id"]
    if messages.delete_message(message_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="")