import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks and handle buy/sell actions"""
    if request.method == "POST":
        # Handle Buy request
        if request.form.get("action") == "buy":
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares"))

            # Validate input
            if not symbol or shares <= 0:
                return apology("must provide a valid stock symbol and a positive number of shares", 400)

            # Lookup stock
            stock = lookup(symbol)
            if stock is None:
                return apology("invalid stock symbol", 400)

            # Check if user has enough cash to buy shares
            total_cost = stock["price"] * shares
            user_cash = db.execute("SELECT cash FROM users WHERE id = ?",
                                   session["user_id"])[0]["cash"]
            if total_cost > user_cash:
                return apology("not enough cash to complete the purchase", 400)

            # Update user's cash balance
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                       total_cost, session["user_id"])

            # Record the purchase
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                session["user_id"], stock["symbol"], shares, stock["price"]
            )

            # Redirect to the portfolio page
            return redirect("/")

        # Handle Sell request
        elif request.form.get("action") == "sell":
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares"))

            # Validate input
            if not symbol or shares <= 0:
                return apology("must provide a valid stock symbol and a positive number of shares", 400)

            # Lookup stock
            stock = lookup(symbol)
            if stock is None:
                return apology("invalid stock symbol", 400)

            # Check if user owns enough shares
            user_shares = db.execute("""
                SELECT SUM(shares) as total_shares
                FROM transactions
                WHERE user_id = ? AND symbol = ?
                GROUP BY symbol
            """, session["user_id"], symbol)

            if len(user_shares) != 1 or user_shares[0]["total_shares"] < shares:
                return apology("not enough shares to sell", 400)

            # Calculate total sale value
            total_sale = stock["price"] * shares

            # Update user's cash balance
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                       total_sale, session["user_id"])

            # Record the sale
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                session["user_id"], stock["symbol"], -shares, stock["price"]
            )

            # Redirect to the portfolio page
            return redirect("/")

    else:
        # Fetch the current stock price for each stock
        rows = db.execute("""
            SELECT symbol, SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
        """, session["user_id"])

        portfolio = []
        total_value = 0
        for row in rows:
            stock = lookup(row["symbol"])
            if stock:
                total_stock_value = stock["price"] * row["total_shares"]
                portfolio.append({
                    "symbol": row["symbol"],
                    "name": stock["name"],
                    "shares": row["total_shares"],
                    "price": stock["price"],
                    "total": total_stock_value
                })
                total_value += total_stock_value

        # Get user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Render index page with portfolio and cash
        return render_template("index.html", portfolio=portfolio, cash=user_cash, total_value=total_value + user_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Get the stock symbol and shares from the form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure stock symbol and shares were provided
        if not symbol:
            return apology("must provide stock symbol", 400)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares", 400)

        # Lookup the stock's current price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Calculate total cost
        total_cost = stock["price"] * int(shares)

        # Get user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Check if user has enough cash
        if total_cost > user_cash:
            return apology("not enough cash", 400)

        # Deduct cost from user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        # Record the purchase in transactions
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
        """, session["user_id"], stock["symbol"], int(shares), stock["price"])

        # Redirect to index after purchase
        return redirect("/")

    else:
        # Render the buy form
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, session["user_id"])

    return render_template("history.html", transactions=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Check if symbol was provided
        if not symbol:
            return apology("must provide a stock symbol", 400)

        # Lookup stock price
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Render a page with the stock's data
        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "POST":
        # Get form inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate form inputs
        if not username:
            return apology("must provide username", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)

        # Check if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(existing_user) > 0:
            return apology("username already exists", 400)

        # Hash the password
        hash_pw = generate_password_hash(password)

        # Insert user into the database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except Exception as e:
            print(f"Database error: {e}")
            return apology("registration failed", 400)

        # Log the user in automatically after registration
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        # Redirect to homepage
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol:
            return apology("must provide stock symbol", 400)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive number of shares", 400)

        # Lookup stock
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid stock symbol", 400)

        # Check if user owns enough shares
        user_shares = db.execute("""
            SELECT SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, session["user_id"], symbol)

        if len(user_shares) != 1 or user_shares[0]["total_shares"] < int(shares):
            return apology("not enough shares to sell", 400)

        # Calculate total sale value
        total_sale = stock["price"] * int(shares)

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, session["user_id"])

        # Record the sale
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], stock["symbol"], -int(shares), stock["price"]
        )

        # Redirect to homepage
        return redirect("/")

    else:
        # Get stocks owned by user
        stocks = db.execute("""
            SELECT symbol, SUM(shares) as total_shares
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING total_shares > 0
        """, session["user_id"])

        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user's account"""
    if request.method == "POST":
        # Get the amount of cash to add from the form
        amount = request.form.get("amount")

        # Ensure amount is a positive number
        if not amount.isdigit() or int(amount) <= 0:
            return apology("must provide a positive amount", 400)

        # Update the user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", int(amount), session["user_id"])

        # Redirect to index after adding cash
        return redirect("/")

    else:
        # Render the add cash form
        return render_template("add_cash.html")


@app.route("/api/symbols")
@login_required
def api_symbols():
    """Provide a list of stock symbols for autocomplete"""
    rows = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?",
                      session["user_id"])
    symbols = [row['symbol'] for row in rows]
    return jsonify(symbols)
