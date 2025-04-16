from flask import Flask, render_template, url_for, request, session, redirect
from chat import chat_with_bot
from mail import gen_random_number, send_email
from database import verify_user, add_user, email_exists, get_name_by_email
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECERT_KEY')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prompting", methods=['GET', 'POST'])
def boom():
    if request.method == 'POST':
        plant_name = request.form.get('plant-name')
        session['plant_name'] = plant_name
        return render_template('loading.html', load_msg="Loading Plant Knowledge AI.....")
    return render_template("boom.html")

@app.route("/chat", methods=['GET', 'POST'])
def chat_page():
    plant_name = session.get('plant_name')
    if request.method == 'POST':
        user_input = request.form.get('user-input')
        bot_output = chat_with_bot(user_input, plant_name)
        return render_template('chat.html', plant_name=plant_name, user_input=user_input, bot_output=bot_output)
    return render_template('chat.html', plant_name=plant_name, user_input='Hi', bot_output = chat_with_bot("Hi", plant_name))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login-email')
        password = request.form.get('login-password')
        if verify_user(email, password):
            name = get_name_by_email(email)
            return render_template('welcome.html', name=name)
        else:
            return render_template('login.html', err_msg="*Incorrect email or password")            
    return render_template('login.html')


@app.route("/email-for-otp")
def email_for_otp():
    return render_template("email.html")

@app.route("/load-otp", methods=['POST', 'GET'])
def load_otp():
    if request.method == 'POST':
        email = request.form.get('otp-email')
        session['email'] = email
        return render_template("loading-otp.html", load_msg=f"Sending OTP to {email}...")
    return render_template("email.html")

@app.route("/send-otp", methods=['POST', 'GET'])
def send_otp():
    email = session.get('email')
    if email_exists(email):
        otp = gen_random_number()
        print(otp)
        send_email(otp, email)
        session['otp'] = otp
        session['email'] = email
        return render_template("otp.html", email=email)
    else:
        return render_template('email.html', err_msg="*No user is linked to that email.")

@app.route("/verify-otp", methods=['POST', 'GET'])
def verify_otp():
    if request.method == 'POST':
        email = session.get('email')
        otp = session.get('otp')
        user_otp = request.form.get('user-otp')
        if str(otp) == user_otp:
            if email_exists(email):
                pass
            else:
                name = session.get('name')
                password = session.get('password')
                add_user(name, email, password)
            return render_template("welcome.html", name=get_name_by_email(email))
        else:
            return render_template('otp.html', email=email, err_msg="*Incorrect OTP")            
    return render_template("otp.html", email=session.get('email'))

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        if password == confirm_password:
            if not(email_exists(email)):
                session['name'] = name
                session['email'] = email
                session['password'] = password
                return render_template("loading-signup-otp.html", load_msg=f"Sending OTP to {email}...")
            else:
                return render_template('signup.html', err_msg="*User with that email already exsist")            
        else:
            return render_template('signup.html', err_msg="*Passwords do not match")            
    
    return render_template("signup.html") 

@app.route("/loading-signup-otp")
def loading_signup_otp():
    otp = gen_random_number()
    session['otp'] = otp
    print(otp)
    email = session.get("email")
    send_email(otp, email)
    return render_template("otp.html", email=email)

@app.route("/resend-otp")
def resend_otp():
    otp = gen_random_number()
    session['otp'] = otp
    print(otp)
    email = session.get('email')
    send_email(otp, email)
    return render_template('otp.html', email=email, err_msg="OTP resent")

@app.route("/loading-resend-otp")
def loading_resend_otp():
    return render_template("loading-resend-otp.html", load_msg=f"Resending OTP to {session.get('email')}...")

@app.route("/landing-otp")
def landing_otp():
    otp = session.get("otp")
    return render_template("landing.html", otp=otp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)