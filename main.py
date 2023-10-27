from flask import session, Flask, render_template, redirect, request, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

from forms import *

app = Flask(__name__)
Bootstrap5(app)

app.config['SECRET_KEY'] = 'secretkey'

"""db connecting"""
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bk.db"
db = SQLAlchemy()
db.init_app(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Accounts, user_id)


class Accounts(UserMixin, db.Model):
    """set savings and current balance default to zero"""
    __tablename__ = "accounts_db"
    id = db.Column(db.Integer, primary_key=True)
    savings_account = db.Column(db.String(250), unique=True, nullable=False)
    checking_account = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)

    savings_balance = db.Column(db.String(250), default="0")
    checking_balance = db.Column(db.String(250), default="0")

    # transaction = relationship("Transactions", back_populates="username")
    # routing_number = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250))
    password = db.Column(db.String(250))
    active = db.Column(db.Boolean, default=True)
    restricted = db.Column(db.Boolean, default=False)
    # account_type = db.Column(db.String(250))
    pin = db.Column(db.String(250))


class Transactions(db.Model):
    __tablename__ = "transactions_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(250))
    date = db.Column(db.String(250))
    amount = db.Column(db.String(250))
    type = db.Column(db.String(250))
    remark = db.Column(db.String(250))


with app.app_context():
    db.create_all()

"""global variables"""


# there are no global variable yet


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    """display sign up form and adds collected data to send as an email to the admin"""
    form = SignUp()

    if form.validate_on_submit():
        return redirect(url_for("signup_success"))
    """this should send all the information the user passed in as an email to the admin as return a success page"""
    return render_template("signup.html", form=form)


@app.route("/signup-successful")
def signup_success():
    return render_template("signup-success.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    users = db.session.execute(db.Select(Accounts)).scalars().all()

    return render_template("admin.html", users=users)


@app.route("/add-transaction", methods=["GET", "POST"])
def add_transaction():
    add_transact = AddTransaction()

    if add_transact.validate_on_submit():
        user = db.session.execute(
            db.select(Accounts).where(Accounts.username == add_transact.username.data)).scalar()
        new_transaction = Transactions(
            user_id=user.id,
            username=user.username,
            date=add_transact.Date.data,
            amount=add_transact.amount.data,
            type=add_transact.type.data,
            remark=add_transact.remark.data

        )
        db.session.add(new_transaction)
        db.session.commit()

        return "NEW BALANCE UPDATED"

    return render_template("add-transaction.html", form=add_transact)


@app.route("/add-accounts", methods=["GET", "POST"])
def add_accounts():
    """creates a new account"""
    add_aza = AddAccount()

    if add_aza.validate_on_submit():
        new_user = Accounts(
            first_name=add_aza.first_name.data,
            last_name=add_aza.last_name.data,
            username=add_aza.username.data,
            password=add_aza.password.data,
            savings_account=add_aza.savings.data,
            checking_account=add_aza.checking.data,
        )

        db.session.add(new_user)
        db.session.commit()

        return "NEW ACCOUNT CREATED"

    return render_template("add-accounts.html", form1=add_aza)


@app.route("/add-money", methods=["GET", "POST"])
def add_money():
    """updates the balance of an account"""
    add_bar = AddMoney()
    # add_transaction = AddTransaction()

    if add_bar.validate_on_submit():
        new_balance = add_bar.amount.data
        user = db.session.execute(db.select(Accounts).where(Accounts.username == add_bar.username.data)).scalar()
        if add_bar.account_type.data == "Checking Account":
            user.checking_balance = new_balance
            db.session.commit()

        else:
            user.savings_balance = new_balance
            db.session.commit()

        return "NEW BALANCE UPDATED"

    return render_template("add-money.html", form2=add_bar)


@app.route("/block-aza", methods=["GET", "POST"])
def block_aza():
    """blocks account due to suspicious activities, displays modal in the profile login page """
    blockaza = BlockAza()
    openaza = OpenAza()
    if blockaza.validate_on_submit():
        user = db.session.execute(db.select(Accounts).where(Accounts.username == blockaza.username.data)).scalar()
        user.active = False
        db.session.commit()

    if openaza.validate_on_submit():
        user = db.session.execute(db.select(Accounts).where(Accounts.username == blockaza.username.data)).scalar()
        user.active = True
        db.session.commit()

    return render_template("block-account.html", form1=blockaza, form2=openaza)


@app.route("/login", methods=["GET", "POST"])
def login():
    """logs in an already registered user and displays their bank account details"""
    form = Login()

    if form.validate_on_submit():
        user = db.session.execute(db.select(Accounts).where(Accounts.username == form.username.data)).scalar()
        print(user)
        if user:
            if form.password.data == user.password:
                login_user(user)
                return redirect(url_for("welcome"))

            else:
                flash("Incorrect Password")
                return redirect(url_for("login"))

        else:
            flash("Username Does not Exist")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/register")
def register():
    """registers a new online user and adds it to the database"""
    form = Register()
    if form.validate_on_submit():
        account_no = form.account_no.data
        username = form.username.data
        password = form.password.data
        confirm_pass = form.confirm_password.data

        if password != confirm_pass:
            flash("Password do not match")
        else:
            user = db.session.execute(db.Select(Accounts).where(Accounts.savings_account == account_no)).scalar()
            user_ = db.session.execute(db.Select(Accounts).where(Accounts.checking_account == account_no)).scalar()

            if user:
                user.username = username
                user.password = password
                db.session.commit()

            elif user_:
                user_.username = username
                user_.password = password
                db.session.commit()

            else:
                flash("Please Make sure you have an account with us or Your account number may be incorrect")

    return render_template("register.html", form=form)


@app.route("/welcome")
def welcome():
    """welcome page after login, shows the account number and balance for both savings and current account,
    also displays the last 3 transactions """

    print(current_user.username)
    account = db.session.execute(db.select(Accounts).where(Accounts.username == current_user.username)).scalar()
    """add active as a booleen field in the accounts database so that you wil not need to pass in active in all the function you can just check if account.active"""
    active = current_user.active
    transactions = (Transactions.query.filter_by(username=current_user.username).limit(3).all())
    return render_template("welcome.html", transactions=transactions, account=account, active=active)


@app.route("/send-money", methods=["GET", "POST"])
def send_money():
    send = False
    otp = False
    acc = ChoseAccount()

    if acc.validate_on_submit():
        session['amount'] = acc.amount.data
        session["account"] = acc.account_no.data

        if acc.account_type.data == "Checking Account":
            if int(current_user.checking_balance) > (int(acc.amount.data) + 5):
                return redirect(url_for("otp_code"))

    return render_template("send-money.html", form=acc, send=send, )


@app.route("/receive-money")
def receive_money():
    return render_template("receive-money.html")


@app.route("/schedule-send")
def schedule():
    confirm = False
    form = ScheduleSend()
    if form.validate_on_submit():
        confirm = True
    return render_template("schedule-send.html", form=form, confirm=confirm)


"""gets otp and checks with otp user types in"""


@app.route("/otp-validation", methods=["GET", "POST"])
def otp_code():
    banking_pin = "123456"
    # print(banking_pin)
    verify = Verify()
    amount = request.form.get("amount")
    account_no = request.form.get("account_no")
    session["amount_"] = amount
    session["account_"] = account_no

    if verify.validate_on_submit():
        code = f'{request.form.get("code1")}{request.form.get("code2")}{request.form.get("code3")}{request.form.get("code4")}{request.form.get("code5")}{request.form.get("code6")}'

        if code == banking_pin:
            """check if the account has been restricted from making transfers, redirect to payment0failed, 
            if not redirect to payment successfully """
            restricted = current_user.restricted
            if restricted:
                return redirect(url_for("payment_failed"))
            else:
                return redirect(url_for("payment_successful"))

    return render_template("otp.html", form=verify, amount=amount, account_no=account_no)


@app.route("/payment-successful", methods=["GET", "POST"])
def payment_successful():
    form = Receipt()
    amount_ = session.get('amount', None)
    account_ = session.get("account", None)
    if amount_ is not None:
        # print("got it first")
        amount = amount_
        account = account_
    else:
        # print("got it last")
        amount = session.get("amount_")
        account = session.get("account_")

    if form.validate_on_submit():
        return redirect(url_for("welcome"))
    return render_template("payment-successful.html", form=form, amount=amount, account=account)


@app.route("/payment-failed")
def payment_failed():
    return render_template("payment-failed.html")


@app.route("/history")
def history():
    transactions = db.session.execute(
        db.select(Transactions).where(Transactions.username == current_user.username)).scalars().all()

    return render_template("history.html", transactions=transactions)


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/customer-service")
def customer_service():
    return render_template("customer-service.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    acc = ChoseAccount()

    if acc.validate_on_submit():
        code1 = request.form.get("code1")
        code2 = request.form.get("code2")
        code3 = request.form.get("code3")
        code4 = request.form.get("code4")
        code5 = request.form.get("code5")
        code6 = request.form.get("code6")
        return f"{code1}, {code2}, {code3}"

    return render_template("test.html", form=acc)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)
