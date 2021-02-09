from discord_webhook import webhook
from flask import *
import pyrebase
from .discord_hook import DiscordAlert

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyCIDZEBPCZFI7pZ7xy5MateMBgYOOqPgLc",
  "authDomain": "anime-disqus-bot.firebaseapp.com",
  "databaseURL": "https://anime-disqus-bot-default-rtdb.firebaseio.com",
  "projectId": "anime-disqus-bot",
  "storageBucket": "anime-disqus-bot.appspot.com",
  "messagingSenderId": "254500274459",
  "appId": "1:254500274459:web:72aac6829f9779c9d213be",
  "measurementId": "G-3SVF0VMR12"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=["POST", "GET"])
def login():
  unsuccess = "Invalid credentials"
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']

    try:
      auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('choice'))
    except:
      return render_template("login.html", us=unsuccess)

  return render_template("login.html")


@app.route('/choice', methods=["POST", "GET"])
def choice():
  if request.method == "POST":
      if request.form['choice'] == "Check User":
        return redirect(url_for('viewuser'))
      elif request.form['choice'] == "Check Comment":
        return redirect(url_for('viewcomment'))
  return render_template("choice.html")


@app.route('/viewcomment', methods=["POST", "GET"])
def viewcomment():
  invalid = "Invalid URL"
  if request.method == "POST":
    if type(request.form['url']) == 'int':
      return "System"
  return render_template("viewcomment.html")


@app.route('/viewuser', methods=["POST", "GET"])
def viewuser():
  return render_template("viewuser.html")

if __name__ == '__main__':
  app.run(debug=True)