from discord_webhook import webhook
from flask import *
import pyrebase
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808249420750520351/7S3GqGkalYuzmNi8M9x6dU3KGjeR40sTbVv0d4ROSwtO_HbrjpBItAuiKfAtCMHtoEuI')

API_KEY = 'LwMepQiQSd2tOCueHzk5rS4fPXA9fgdlpwPHAEvxYHMpQYPkfmhFw7PpRSa5lmsR'

class DiscordAlert:
    def __init__(self, comment_id):

        global API_KEY

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}'.format(API_KEY, comment_id)
        
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
  error = None
  if request.method == "POST":
    email = request.form['email']
    password = request.form['password']

    try:
      auth.sign_in_with_email_and_password(email, password)
      return redirect(url_for('choice'))
    except:
      error = "Invalid credentials"
      return render_template("login.html", error=error)

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
  error = None
  if request.method == "POST":
      try:
        comment_id = int(request.form['commentid'])

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}'.format(API_KEY, comment_id)
        
        response = requests.get(url)
        response = json.loads(response.text)

        if response['response']['forum'] != '9anime-to':
          raise Exception

        user_data = {
          'displayname':response['response']['author']['name'],
          'username':response['response']['author']['name'],
          'content':response['response']['message']
        }
        
        #alert = DiscordAlert(comment_id)
        #alert.send_alert()
      except Exception as e:
        print(e)
        error = "Invalid Comment ID"
        return render_template('viewcomment.html', error=error)
  return render_template("viewcomment.html")


@app.route('/viewuser', methods=["POST", "GET"])
def viewuser():
  return render_template("viewuser.html")

if __name__ == '__main__':
  app.run(debug=True)