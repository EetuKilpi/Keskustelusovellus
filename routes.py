from app import app
from flask import render_template, request, redirect
import messages, users


@app.route("/")
def index():
    message = messages.get_list()
    user_id = users.user_id()
    favorite = []
    if user_id != 0:
        favorite = messages.get_favorite_message_ids(user_id)
    admin = users.is_admin()
    if admin == None:
        admin = False
    all_messages_private = True
    for i in message:
        if i[-1] == False:
            all_messages_private = False
    if message == []:
        message = None
    if all_messages_private == True and admin != True:
        message = None
    return render_template("index.html", messages=message, favorites=favorite, admin=admin)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_private")
def new_private():
    admin = users.is_admin()
    return render_template("new_private.html", admin = admin)

@app.route("/send", methods=["POST"])
def send():
    topic = request.form["topic"]
    text = request.form["text"]
    privacy = request.form["privacy"]
    if messages.send(topic, text, privacy):
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
    admin = users.is_admin()
    return render_template("answer.html", message=list, answers=list2, admin=admin)

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
    user_id = users.user_id()
    admin = users.is_admin()
    if admin == None:
        admin = False
    favorite = []
    if user_id != 0:
        favorite = messages.get_favorite_message_ids(user_id)
    counter = 0
    if query != "":
        message = messages.search(query)
        for i in message:
            if i[8] == True:
                counter += 1
    return render_template("result.html", messages=message ,query=query, admin=admin, counter=counter, favorites=favorite)

@app.route("/delete_answer", methods=["POST"])
def delete_answer():
    allow = False
    answer_id = request.form["answer_id"]
    message_id = request.form["message_id"]
    user_id = request.form["user_id"]
    if users.is_admin():
        allow = True
    if messages.allow_user(user_id, answer_id, 1):
        allow = True
    if allow == True:
        messages.delete_answer(answer_id)
        return redirect("/message/" + str(message_id))
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="message/"+str(message_id))

@app.route("/delete_message", methods=["POST"])
def delete_message():
    allow = False
    user_id = request.form["user_id"]
    message_id = request.form["message_id"]
    if users.is_admin():
        allow = True
    if messages.allow_user(user_id, message_id, 0):
        allow = True
    if allow == True:
        messages.delete_message(message_id)
        return redirect("/")
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="")

@app.route("/edit_answer/<int:answer_id>", methods=["GET", "POST"])
def edit_answer(answer_id):
    message_id = request.args.get("message_id")
    user_id = request.args.get("user_id")
    
    if messages.allow_user(user_id, answer_id, 1):
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
    
    if messages.allow_user(user_id, message_id, 0):
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

@app.route("/add_favorite", methods=["POST"])
def favorite_message():
    user_id = request.form["user_id"]
    message_id = request.form["message_id"]
    source = request.form["source"]
    if messages.add_favorite(message_id, user_id):
        return redirect(source)
    else:
        return render_template("error.html", message="Viestin lisääminen epäonnistui", url="")

@app.route("/favorites")
def favorites():
    user_id = users.user_id()
    admin = users.is_admin()
    if admin == None:
        admin = False
    if user_id != 0:
        favorite_messages = messages.get_favorite_messages(user_id)
        all_messages_private = True
        for i in favorite_messages:
            if i[-1] == False:
                all_messages_private = False
        if favorite_messages == []:
            favorite_messages = None
        if all_messages_private == True and admin != True:
            favorite_messages = None
        return render_template("favorites.html", messages=favorite_messages)
    else:
        return render_template("error.html", message="Kirjaudu ensin sisään nähdäksesi suosikkiviestisi", url="login")

@app.route("/remove_favorite", methods=["POST"])
def remove_favorite():
    user_id = request.form["user_id"]
    message_id = request.form["message_id"]
    source = request.form["source"]
    if messages.remove_favorite(message_id, user_id):
        return redirect(source)
    else:
        return render_template("error.html", message="Suosikin poistaminen epäonnistui", url="favorites")

@app.route("/polls")
def polls():
    poll = messages.get_polls()
    if poll == []:
        poll = None
    return render_template("polls.html", polls=poll)

@app.route("/new_poll")
def new_poll():
    return render_template("new_poll.html")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    poll_id = messages.create_poll(topic)
    choices = request.form.getlist("choice")
    if poll_id != False:
        if messages.create_choices(poll_id, choices):
            return redirect("/polls")
        else:
            return render_template("error.html", message="Kyselyn luominen epäonnistui", url="polls")
    else:
        return render_template("error.html", message="Kyselyn luominen epäonnistui", url="polls")

@app.route("/poll/<int:id>")
def poll(id):
    topic = messages.get_poll_topic(id)
    choices = messages.get_poll_choices(id)
    return render_template("poll.html", id=id, topic=topic, choices=choices)

@app.route("/poll_answer", methods=["POST"])
def poll_answer():
    poll_id = request.form["id"]
    if "poll_answer" in request.form:
        choice_id = request.form["poll_answer"]
        if messages.poll_answer(choice_id):
            return redirect("/poll_result/" + str(poll_id))
        else:
            return render_template("error.html", message="Kyselyn luominen epäonnistui", url="polls")

@app.route("/poll_result/<int:id>")
def poll_result(id):
    topic = messages.get_poll_topic(id)
    choices = messages.get_poll_results(id)
    last_answer = messages.get_last_poll_answer(id)
    return render_template("poll_result.html", topic=topic, choices=choices, last_answer=last_answer)

@app.route("/delete_poll", methods=["POST"])
def delete_poll():
    allow = False
    user_id = request.form["user_id"]
    poll_id = request.form["poll_id"]
    if users.is_admin():
        allow = True
    if messages.allow_user(user_id, poll_id, 2):
        allow = True
    if allow == True:
        messages.delete_poll(poll_id)
        return redirect("/polls")
    else:
        return render_template("error.html", message="Sinulla ei ole oikeuksia tähän", url="polls")