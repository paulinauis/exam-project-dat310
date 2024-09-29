from setup_db import *
from flask import Flask, render_template, url_for, redirect, request, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from forms import PostForm
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'a csrf secret key'

# Function to connect to the database, from ex2 lecture 04.04
def get_db():
    if not hasattr(g, "_database"):
        g._database = sqlite3.connect("./data/database.db")
        g._database.row_factory = sqlite3.Row
    return g._database

# Function to disconnect from the database, from ex2 lecture 04.04
@app.teardown_appcontext
def teardown_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT email FROM admins")
    admins = [row['email'] for row in cur.fetchall()]

    # Hent det siste innlegget
    cur.execute("SELECT * FROM posts ORDER BY publish_date DESC LIMIT 1")
    latest_post = cur.fetchone()

    return render_template("index.html", admins=admins, latest_post=latest_post)


@app.route("/index")
def hjem():
    email = session.get("email")
    return render_template("index.html", email=email)


@app.route("/create_post", methods=['GET', 'POST'])
def create_post():
    if 'email' not in session:
        flash("Du må logge inn som admin for å opprette innlegg.", "danger")
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT admin_id FROM admins WHERE email = ?", (session['email'],))
    admin = cur.fetchone()

    if not admin:
        flash("Du har ikke tilgang til å opprette innlegg.", "danger")
        return redirect(url_for('index'))
    
    form = PostForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
        
        cur.execute(
            "INSERT INTO posts (title, image, body, tags, publish_date, admin_id) VALUES (?, ?, ?, ?, ?, ?)",
            (form.title.data, image_file, form.body.data, form.tags.data, datetime.datetime.now().strftime("%Y-%m-%d"), admin['admin_id'])
        )
        conn.commit()
        flash("Innlegget er publisert!", "success")
        return redirect(url_for('innlegg'))
    return render_template('create_post.html', title="Nytt Innlegg", form=form)


@app.route("/delete_post/<int:post_id>", methods=['POST'])
def delete_post(post_id):
    if 'email' not in session:
        flash("Du må være logget inn som admin for å slette innlegg.", "danger")
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # sjekk om brukeren som er logget inn er admin
    cur.execute("SELECT admin_id FROM admins WHERE email = ?", (session['email'],))
    admin = cur.fetchone()

    if not admin:
        flash("Du har ikke tilgang til å slette innlegg.", "danger")
        return redirect(url_for('index'))

    # sjekk om innlegget finnes
    cur.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
    post = cur.fetchone()

    if not post:
        flash("Innlegget eksisterer ikke.", "danger")
        return redirect(url_for('innlegg'))
    
    if post['admin_id'] != admin['admin_id']:
        flash("Du har ikke tillatelse til å slette dette innlegget.", "danger")
        return redirect(url_for('innlegg'))

    # slett innlegget
    cur.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
    conn.commit()
    flash("Innlegget er slettet!", "success")
    return redirect(url_for('innlegg'))


@app.route("/innlegg")
def innlegg():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()

    # Kode for å hente inn epost verdi til alle admins 
    cur.execute("SELECT email FROM admins")
    admins = [row['email'] for row in cur.fetchall()]
    return render_template("innlegg.html", posts=posts, admins=admins)


@app.route("/sofie")
def sofie():
    return render_template("sofie.html")

@app.route("/paulina")
def paulina():
    return render_template("paulina.html")

@app.route("/anette")
def anette():
    return render_template("anette.html")

@app.route("/lisbeth")
def lisbeth():
    return render_template("lisbeth.html")


@app.route("/kontakt")
def kontakt():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT email FROM admins")
    admins = [row['email'] for row in cur.fetchall()]
    return render_template("kontakt.html", admins=admins)


@app.route("/oss")
def oss():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT email FROM admins")
    admins = [row['email'] for row in cur.fetchall()]
    return render_template("oss.html", admins=admins)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["email"] = email  # Set session variable upon successful login
            session["first_name"] = user["first_name"]  # Set first name in session
            #flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid email and/or password", "error")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("email", None)  # Remove the "email" session variable
    return redirect(url_for("index"))  # Redirect to the home page after logout

# Oppdatert sign_up-rute for å bruke SQLite
@app.route('/registrer', methods=['GET', 'POST'])
def registrer():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

        if user:
            flash('Email finnes allerede i databasen.', category='error')
        elif len(email) < 4:
            flash('Email må ha flere enn 3 tegn.', category='error')
        elif len(first_name) < 2:
            flash('Navn må ha mer enn ett tegn.', category='error')
        elif password1 != password2:
            flash('Passord stemmer ikke', category='error')
        elif len(password1) < 7:
            flash('Passord må ha minst 7 tegn.', category='error')
        else:
            password_hash = generate_password_hash(password1, method='pbkdf2:sha256')
            cur.execute("INSERT INTO users (email, first_name, password_hash) VALUES (?, ?, ?)",
                        (email, first_name, password_hash))
            conn.commit()
            flash('Bruker lagret! Nå kan du logge inn!', category='success')

    return render_template('registrer.html')

@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get('email')
    if email=="":
        flash("Du må skrive inn e-post adresse!", category='error')
    else:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO subscriptions (email, subscribed) VALUES (?, ?)", (email, True))
        conn.commit()
        flash("Takk for at du abonnerer!", category='success')
    return redirect(url_for('index'))

@app.route("/edit_post/<int:post_id>", methods=['GET', 'POST'])
def edit_post(post_id):
    if 'email' not in session:
        flash("Du må være logget inn som admin for å redigere innlegg.", "danger")
        return redirect(url_for('login'))

    conn = get_db()
    cur = conn.cursor()

    # Sjekk om brukeren som er logget inn er admin
    cur.execute("SELECT admin_id FROM admins WHERE email = ?", (session['email'],))
    admin = cur.fetchone()

    if not admin:
        flash("Du har ikke tilgang til å redigere innlegg.", "danger")
        return redirect(url_for('innlegg'))

    # Sjekk om innlegget finnes
    cur.execute("SELECT * FROM posts WHERE post_id = ?", (post_id,))
    post = cur.fetchone()

    if not post:
        flash("Innlegget eksisterer ikke.", "danger")
        return redirect(url_for('innlegg'))
    
    if post['admin_id'] != admin['admin_id']:
        flash("Du har ikke tillatelse til å redigere dette innlegget.", "danger")
        return redirect(url_for('innlegg'))

    # Opprett et skjema for redigering av innlegget
    form = PostForm()

    # Fyll inn skjemaet med eksisterende innholdsdata
    form.title.data = post['title']
    form.body.data = post['body']
    form.tags.data = post['tags']

    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
        
        # Oppdater innlegget i databasen
        cur.execute(
            "UPDATE posts SET title = ?, image = ?, body = ?, tags = ?, publish_date = ? WHERE post_id = ?",
            (form.title.data, image_file, form.body.data, form.tags.data, datetime.datetime.now().strftime("%Y-%m-%d"), post_id)
        )
        conn.commit()
        flash("Innlegget er oppdatert!", "success")
        return redirect(url_for('innlegg'))
    
    # Returner skjemaet for redigering av innlegget
    return render_template('edit.html', title="Rediger Innlegg", form=form)


if __name__ == "__main__":
    app.run(debug=True)


"""
Innlegg til presentasjonen: 
- lag ny bruker 
- logg inn som bruker 
- logg inn som admin og publiser, rediger og slett et innlegg
- abonner på nyhetsbrev 
- vis mobilversjon av siden 
- TA SOMMERFERIE
"""
