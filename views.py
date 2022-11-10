# from flask import Blueprint, render_template
# from forms import RegistrationForm, LoginForm
# views = Blueprint(__name__, "views")
#
# @views.route("/")
# @views.route("/index")
# def home():
#     return render_template("index.html")
#
# @views.route("/predict")
# def predict():
#     return render_template("risk_predict.html")
#
# @views.route("/blog")
# def blog():
#     return render_template("single-blog.html")
#
# @views.route("/about")
# def about():
#     return render_template("about-us.html")
#
# @views.route("/doctors")
# def doctors():
#     return render_template("doctors.html")
#
# @views.route("/register")
# def register():
#     form = RegistrationForm()
#     return render_template("register.html", title='Register', form=form)
#
# @views.route("/login")
# def register():
#     form = LoginForm()
#     return render_template("login.html", title='Login', form=form)
