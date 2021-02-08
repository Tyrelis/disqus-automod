import pyrebase
from flask import *

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
  return render_template("choice.html")



if __name__ == '__main__':
  app.run()