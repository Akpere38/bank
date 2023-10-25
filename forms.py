from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, DateField, \
    BooleanField, FileField, TimeField
from wtforms.validators import DataRequired, Email


class SignUp(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    sex = SelectField("Gender", choices=["Male", "Female", "Others"], validators=[DataRequired()])
    dob = DateField("Date of Birth", validators=[DataRequired()])
    ssn = PasswordField("Social Security Number", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    account = SelectField("Account Type",
                          choices=["Savings", "Checking Account", "Business Account", "Foreign Currency Account"]
                          , validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    zip_code = StringField("Zipcode", validators=[DataRequired()])
    id_card = FileField("Upload a Valid ID card", validators=[DataRequired()])
    info = BooleanField("I agree that all the information above are correct", validators=[DataRequired()])
    tmc = BooleanField("I agree to the terms and conditions ", validators=[DataRequired()])
    sign_up = SubmitField("Sign Up")


class Login(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Log in")


class Register(FlaskForm):
    account_no = StringField(label="Account Number", validators=[DataRequired()])
    username = StringField(default="Username", validators=[DataRequired()])
    password = PasswordField(default="Password", validators=[DataRequired()])
    confirm_password = PasswordField(default="Confirm Password", validators=[DataRequired()])
    tmc = BooleanField("By clicking Register, you agree to all the terms and conditions")
    register = SubmitField("Register")


class ChoseAccount(FlaskForm):
    account_type = SelectField("Select your Account", choices=["Checking Account", "Savings Account"],
                               validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    account_no = StringField("Receivers Account Number", validators=[DataRequired()])
    routing_no = StringField("Routing Number", validators=[DataRequired()])
    receivers_name = StringField("Receivers Account Name", validators=[DataRequired()])
    bank_name = StringField("Bank Name", validators=[DataRequired()])
    bank_address = StringField("Bank Address", render_kw={"placeholder": "If required"})
    narration = StringField("Narration", validators=[DataRequired()])
    send = SubmitField("Send")


class ScheduleSend(FlaskForm):
    account_type = SelectField("Select your Account", choices=["Checking Account", "Savings Account"],
                               validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    account_no = StringField("Receivers Account Number", validators=[DataRequired()])
    routing_no = StringField("Routing Number", validators=[DataRequired()])
    receivers_name = StringField("Receivers Account Name", validators=[DataRequired()])
    bank_name = StringField("Bank Name", validators=[DataRequired()])
    bank_address = StringField("Bank Address", render_kw={"placeholder": "If required"})
    narration = StringField("Narration", validators=[DataRequired()])
    date = DateField("Send on this Date", validators=[DataRequired()])
    time = TimeField("Send on this Time", validators=[DataRequired()])
    send = SubmitField("Confirm Schedule")


class Verify(FlaskForm):
    yes = SubmitField("Validate")
    # no = SubmitField("No")


class Receipt(FlaskForm):
    yes = SubmitField("OK")


class AddAccount(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    savings = StringField(label="Savings Account ", validators=[DataRequired()])
    checking = StringField(label="Checking Account ", validators=[DataRequired()])
    username = StringField(default="Username", validators=[DataRequired()])
    password = PasswordField(default="Password", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    add = SubmitField("ADD")


class AddMoney(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    account_type = SelectField("Select your Account", choices=["Checking Account", "Savings Account"],
                               validators=[DataRequired()])
    account_no = StringField(label="Account Number", validators=[DataRequired()])
    amount = StringField(label="Amount", validators=[DataRequired()])
    add = SubmitField("ADD")


class AddTransaction(FlaskForm):
    account_no = StringField(label="Account Number", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    Date = StringField(label=" Date", validators=[DataRequired()])
    type = StringField(label="Type", validators=[DataRequired()])
    amount = StringField(label="Amount", validators=[DataRequired()])
    remark = StringField(label="Remark", validators=[DataRequired()])
    add = SubmitField("ADD")


class BlockAza(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    submit = SubmitField("Block")


class OpenAza(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    submit = SubmitField("Unblock")


class PaymentFailed(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    stop_payment = SubmitField("Stop Payment")


