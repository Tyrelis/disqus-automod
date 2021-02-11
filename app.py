from flask import *
from flask_mysqldb import MySQL, MySQLdb
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook
import requests
import json
import bcrypt

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808249420750520351/7S3GqGkalYuzmNi8M9x6dU3KGjeR40sTbVv0d4ROSwtO_HbrjpBItAuiKfAtCMHtoEuI')

API_KEY = 'LwMepQiQSd2tOCueHzk5rS4fPXA9fgdlpwPHAEvxYHMpQYPkfmhFw7PpRSa5lmsR'
access_token = 'a0f18fb3e52643eeb79ee4e5535bed88'

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = '9animedb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

class DiscordAlert:

    global API_KEY
    global access_token

    def __init__(self, comment_id):        

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY,
                                                                                                        comment_id,
                                                                                                        access_token)
        
        response = requests.get(url)
        response = json.loads(response.text)

        if response['response']['forum'] != '9anime-to':
          raise Exception
        
        self.user = response['response']['author']['username']
        self.comment_id = comment_id
        self.timeout_duration = "1 Days"
        self.mod = "Kenny Senpai"
        self.comment_url = 'https://9anime-to.disqus.com/admin/moderate/all/search/id:{}'.format(comment_id)

    def send_alert(self):
        embed = DiscordEmbed(title='Timeout Issued',
                            color=0x5A2E98)

        embed.set_author(name="View Comment", url=self.comment_url)

        embed.add_embed_field(name="User", value=self.user)
        embed.add_embed_field(name="Comment ID", value=self.comment_id)
        embed.add_embed_field(name="Timeout Duration", value=self.timeout_duration)
        embed.add_embed_field(name="Moderator", value=self.mod)

        webhook.add_embed(embed)
        response = webhook.execute()

'''config = {
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
auth = firebase.auth()'''

@app.route('/', methods=["POST", "GET"])
def login():
  error = None
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password'].encode('utf-8')

    try:
      curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      curl.execute("SELECT * FROM mods WHERE username=%s",(username,))
      user = curl.fetchone()
      curl.close()

      if user:
        if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
          session['name'] = user['username']
          return redirect(url_for('choice'))
        else:
          error = "Invalid credentials"
          return render_template("login.html", error=error)
      else:
        error = "Invalid credentials"
        return render_template("login.html", error=error)
    except Exception as e:
      error = "An error occurred."
      print(e)
      return render_template("login.html", error=error)

  return render_template("login.html")


'''@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO mods (username, password) VALUES (%s,%s)",(name,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        return redirect(url_for('login'))
'''

@app.route('/choice', methods=["POST", "GET"])
def choice():
  if session.get('name'):
    if request.method == "POST":
        if request.form['choice'] == "Check User":
          return redirect(url_for('viewuser'))
        elif request.form['choice'] == "Check Comment":
          return redirect(url_for('viewcomment'))
    return render_template("choice.html")
  else:
    error = "Unauthorized Access."
    return render_template("login.html", error=error)


@app.route('/viewcomment', methods=["POST", "GET"])
def viewcomment():
  error = None
  if request.method == "POST":
      try:
        comment_id = int(request.form['commentid'])

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}'.format(API_KEY, comment_id)
        
        response = requests.get(url)
        response = json.loads(response.text)

        if response['response']['forum'] != '9anime-to':
          raise Exception

        #return redirect(url_for('comment', comment_id = comment_id))

        alert = DiscordAlert(comment_id)
        alert.send_alert()
      except Exception as e:
        print(e)
        error = "Invalid Comment ID"
        return render_template('viewcomment.html', error=error)
  return render_template("viewcomment.html")

@app.route('/check_comment/<int:comment_id>/', methods=["POST", "GET"])
def comment(comment_id):
  url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}'.format(API_KEY, comment_id)
        
  response = requests.get(url)
  response = json.loads(response.text)

  if response['response']['forum'] != '9anime-to':
    return redirect(url_for('not_found'))

  user_data = {
          'display_name':response['response']['author']['name'],
          'username':response['response']['author']['name'],
          'content':response['response']['message'],
          'upvotes':response['response']['likes'],
          'downvotes':response['response']['likes'],
        }
  return render_template("comment.html", comment_id = comment_id, user_data = user_data)

@app.route('/viewuser', methods=["POST", "GET"])
def viewuser():
  return render_template("viewuser.html")

@app.route('/404')
def not_found():
  return render_template("404.html")

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':

  app.secret_key = 'lol'
  app.run(debug=True)