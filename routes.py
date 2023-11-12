from app import app
from flask import render_template, request, redirect
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
        return render_template("error.html", message="Viestin lähetys ei onnistunut",url="")

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