from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
import os
import pyrebase
# from views import views

app = Flask(__name__)

config = {
    'apiKey': "AIzaSyAXDVa8SLmde-ISlPy5S65DVKYOA4mFM4k",
    'authDomain': "rm-flask-project.firebaseapp.com",
    'projectId': "rm-flask-project",
    'storageBucket': "rm-flask-project.appspot.com",
    'messagingSenderId': "868092994632",
    'appId': "1:868092994632:web:c66272d761501ed18b647d",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'

# app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'
# app.register_blueprint(views, url_prefix="/")

model=pickle.load(open('model2.pkl','rb'))

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    return render_template("risk_predict.html")

@app.route("/blog")
def blog():
    return render_template("single-blog.html")

@app.route("/about")
def about():
    return render_template("about-us.html")

@app.route("/doctors")
def doctors():
    return render_template("doctors.html")



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pw1 = request.form['user_pw1']
        pw2 = request.form['user_pw2']
        if pw1 == pw2:
            try:
                email = request.form['user_email']
                password = request.form['user_pw1']
                new_user = auth.create_user_with_email_and_password(email,password)
                auth.send_email_verification(new_user['idToken'])
                return render_template('verify_email.html')
            except:
                existing_account = 'This email is already used'
                return render_template('register.html', exist_message=existing_account)
        else:
            existing_account = 'Passwords are Unmatched'
            return render_template('register.html', exist_message=existing_account)
    return render_template("register.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_pw']
        try:
            auth.sign_in_with_email_and_password(email, password)
            user_info = auth.sign_in_with_email_and_password(email, password)
            account_info = auth.get_account_info(user_info['idToken'])
            if account_info['user'][0]['emailVerified'] == False:
                verify_message = 'Please Verify Your Email'
                return render_template('login.html', umessage=verify_message)
            return render_template('index.html')
        except:
            unsuccessful = 'Please Check Your Credentials'
            return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['user_email']
        auth.send_password_reset_email(email)
        return render_template('login.html')
    return render_template('reset_password.html')


@app.route('/predict',methods=['POST','GET'])
def predict2():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)

    if output>str(0.5):
        return render_template('risk_predict.html', pred='You are in Danger Zone.\nColon Cancer Risk is {}'.format(output))
    else:
        return render_template('risk_predict.html', pred='Your are in Safe Zone.\n Colon Cancer Risk is {}'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
