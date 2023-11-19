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
            return render_template("error.html", message="Rekisteröinti ei onnistunut / Käyttäjänimi on jo varattu",url="register")

@app.route("/message/<int:id>")
def message(id):
    list = messages.get_message(id)
    list2 = messages.get_answer(id)
    return render_template("answer.html", message=list, answers=list2)

@app.route("/answer", methods=["POST"])
def answer():
    message_id = request.form["id"]
    texts = request.form["text"]
    if messages.send_answer(message_id, texts):
        return redirect("/message/" + str(message_id))
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut", url="message/"+str(message_id))

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
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="message/"+str(message_id))

@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_id = request.form["message_id"]
    if messages.delete_message(message_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="")

@app.route("/edit_answer/<int:answer_id>", methods=["GET", "POST"])
def edit_answer(answer_id):
    message_id = request.args.get("message_id")
    user_id = request.args.get("user_id")
    
    if messages.allow_edit(user_id, answer_id, 1):
        if request.method == "GET":
                answer = messages.edit_answer(answer_id)
                return render_template("edit_answer.html", answer=answer)

        elif request.method == "POST":
                message_id = request.form["message_id"]
                new_text = request.form["new_text"]
                if messages.update_answer(answer_id,new_text):
                    return redirect("/message/"+str(message_id))
                else:
                    return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="message/"+str(message_id))
    else:   
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="message/"+str(message_id))

@app.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    user_id = request.args.get("user_id")
    
    if messages.allow_edit(user_id, message_id, 0):
        if request.method == "GET":
                message = messages.edit_message(message_id)
                return render_template("edit_message.html", message=message)

        elif request.method == "POST":
                new_topic = request.form["new_topic"]
                new_text = request.form["new_text"]
                if messages.update_message(message_id,new_topic,new_text):
                    return redirect("/")
                else:
                    return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="")
    else:   
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="")