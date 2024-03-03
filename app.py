from flask import Flask, render_template, request, redirect, session
from cs50 import SQL 
from flask_session import Session


app = Flask(__name__)


db = SQL("sqlite:///books.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return render_template("error.html", message = "Nema naziva")
        
        price = request.form.get("price")
        if not price:
            return render_template("error.html", message = "Nema cijene")
        
        db.execute("INSERT INTO books(title, price)VALUES(?, ?)", title,price)

        return render_template("success.html")
    
    return render_template("add.html")

@app.route("/store")
def store():
    books = db.execute("SELECT * FROM books")
    return render_template("store.html", books = books) 

@app.route("/cart", methods = ["GET", "POST"])
def cart():
    
    if "cart" not in session:
        session["cart"] = []

    if request.method == "POST":
        id = request.form.get("id")
        if id:
            session["cart"].append(id)
        return redirect("/cart")
    
    books = db.execute("SELECT * FROM books WHERE id IN (?)", session["cart"])

    return render_template("cart.html", books = books)

@app.route("/pay")
def pay():
    return render_template("pay.html")