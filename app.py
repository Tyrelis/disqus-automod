from flask import *
from flask_mysqldb import MySQL, MySQLdb
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
import bcrypt
import datetime
import re

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
    
    def __init__(self, comment_id, reason, timeout = 0):

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY,
                                                                                                        comment_id,
                                                                                                        access_token)
        
        response = requests.get(url)
        response = json.loads(response.text)
        
        if response['response']['forum'] != '9anime-to':
            raise Exception
        
        self.user = response['response']['author']['username']
        self.comment_id = int(comment_id)
        self.reason = reason
        self.timeout_days = int(timeout)

        cleanr = re.compile('<.p*?>')
        message = re.sub(cleanr, '', response['response']['message'].replace('&amp;', 'and').replace('&lt;', '<').replace('&gt;', '>'))

        self.message = message
        self.editabletime = response['response']['editableUntil']
        self.mod = session.get('name')
        print(self.mod)
        self.comment_url = 'https://9anime-to.disqus.com/admin/moderate/all/search/id:{}'.format(comment_id)

    def send_alert_timeout(self):

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808262501468078080/S9yHoMFDxedcrxQRp2vbZnc2ctAQttVD70X9EGr_d5HlykAVOaBMNSBpmy2BJzssoMt8')

        embed = DiscordEmbed(title='Timeout Issued', color=0x5A2E98)

        embed.set_author(name="View Comment", url=self.comment_url)

        embed.add_embed_field(name="User", value=self.user)
        embed.add_embed_field(name="Comment ID", value=self.comment_id)
        embed.add_embed_field(name="Timeout Duration", value="{} Days".format(self.timeout_days))
        embed.add_embed_field(name="Reason", value=self.reason)
        embed.add_embed_field(name="Moderator", value=self.mod)

        webhook.add_embed(embed)
        response = webhook.execute()

        print("Timeout Sent = {}".format(session.get('name')))
        
    def send_alert_ban(self):

        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808262501468078080/S9yHoMFDxedcrxQRp2vbZnc2ctAQttVD70X9EGr_d5HlykAVOaBMNSBpmy2BJzssoMt8')
        
        embed = DiscordEmbed(title='Permanent Ban Issued', color=0x5A2E98)

        embed.set_author(name="View Comment", url=self.comment_url)

        embed.add_embed_field(name="User", value=self.user)
        embed.add_embed_field(name="Comment ID", value=self.comment_id)
        embed.add_embed_field(name="Reason", value=self.reason)
        embed.add_embed_field(name="Moderator", value=self.mod)

        webhook.add_embed(embed)
        response = webhook.execute()

        print("Ban Sent = {}".format(session.get('name')))
        
    def timeout(self): 
        
        isEditable = datetime.datetime.strptime(self.editabletime, '%Y-%m-%dT%H:%M:%S') > datetime.datetime.now()
            
        url_delete_comment = 'https://disqus.com/api/3.0/posts/remove.json?api_key={}&post={}&access_token={}'.format(API_KEY,
                                                                                                        self.comment_id,
                                                                                                        access_token)
        
        ban_reason = self.reason +" - "+ self.mod
        
        timeout_duration = (datetime.datetime.now() + datetime.timedelta(days=self.timeout_days)).strftime('%Y-%m-%d %H:%M:%S')

        print(isEditable)

        if isEditable:
            
            timeout_message = '''<a><b>This comment has been deleted for violating <a href="https://docs.google.com/document/d/1QXiKpWgGlhA75JNsPy8BltOdNahks61guas3zOQLpis/edit"><b><u>9Anime Comment Policy</u></b></a>.<br><br>You have been given a TimeOut ban for {} Day(s) and ONE warning point. If you're given TWO warning points within the next 30 days, you will be banned.<br>Warned by: {}<br>Reason: {}<br><br>Think you've been wrongly warned? <a href="https://discord.gg/9anime"><b>Post an appeal!</b></a><br>--------------------------------------------------</b><br>'''.format(self.timeout_days, self.mod, self.reason)
            
            url_vote = 'https://disqus.com/api/3.0/posts/vote.json?api_key={}&post={}&access_token={}&vote=1'.format(API_KEY,
                                                                                                        self.comment_id,
                                                                                                        access_token)
            
            url_editcomment = 'https://disqus.com/api/3.0/posts/update.json?api_key={}&post={}&access_token={}&message={}'.format(API_KEY,
                                                                                                                                 self.comment_id,
                                                                                                                                 access_token,
                                                                                                                                 timeout_message+self.message)
            self.edited = requests.post(url_editcomment)
            self.upvoted = requests.post(url_vote)
            
        else: 
            timeout_message = '''Your comment has been deleted for violating <a href="https://docs.google.com/document/d/1QXiKpWgGlhA75JNsPy8BltOdNahks61guas3zOQLpis/edit"><b><u>9Anime Comment Policy</u></b></a>.<br><br>You have been given a TimeOut ban for {} Day(s) and ONE warning point. If you're given TWO warning points within the next 30 days, you will be banned.<br><br>Username: @{}:disqus<br>Warned By: {}<br>Reason: {}<br>Your Comment: <spoiler>{}</spoiler>'''.format(self.timeout_days, self.user, self.mod, self.reason, self.message)
            
            url_post = 'https://disqus.com/api/3.0/posts/create.json?api_key={}&thread={}&access_token={}&message={}'.format(API_KEY,
                                                                                                                            6292105195,
                                                                                                                            access_token,
                                                                                                                            timeout_message)
            self.posted = requests.post(url_post)
            
            print("Posted = {}".format(self.posted))
            
        url_ban_user = 'https://disqus.com/api/3.0/forums/block/banPostAuthor.json?api_key={}&post={}&access_token={}&dateExpires={}&notes={}&banEmail=1&banUser=1'.format(
                                                                                                                                 API_KEY,
                                                                                                                                 self.comment_id,
                                                                                                                                 access_token,
                                                                                                                                 timeout_duration,
                                                                                                                                 ban_reason)
            
        self.deleted = requests.post(url_delete_comment)
        self.banned = requests.post(url_ban_user)

        print("Deleted = {}".format(self.deleted))
        print("Banned = {}".format(self.banned))
        
        self.send_alert_timeout()

    def ban(self):
        
        isEditable = datetime.datetime.strptime(self.editabletime, '%Y-%m-%dT%H:%M:%S') > datetime.datetime.now()
            
        url_delete_comment = 'https://disqus.com/api/3.0/posts/remove.json?api_key={}&post={}&access_token={}'.format(API_KEY,
                                                                                                        self.comment_id,
                                                                                                        access_token)
        
        ban_reason = self.reason +" - "+ self.mod

        print(isEditable)

        if isEditable:
            
            ban_message = '''<a><b>This comment has been deleted for violating <a href="https://docs.google.com/document/d/1QXiKpWgGlhA75JNsPy8BltOdNahks61guas3zOQLpis/edit"><b><u>9Anime Comment Policy</u></b></a><br><br>You have been banned.<br>Banned by: {}<br>Reason: {}<br><br>Think you've been wrongly banned? <a href="https://discord.gg/9anime"><b>Post an appeal</b></a><br>---------------------------------------------------</b><br>'''.format(self.mod, self.reason)
            
            url_vote = 'https://disqus.com/api/3.0/posts/vote.json?api_key={}&post={}&access_token={}&vote=1'.format(API_KEY,
                                                                                                        self.comment_id,
                                                                                                        access_token)
            
            url_editcomment = 'https://disqus.com/api/3.0/posts/update.json?api_key={}&post={}&access_token={}&message={}'.format(API_KEY,
                                                                                                                                 self.comment_id,
                                                                                                                                 access_token,
                                                                                                                                 ban_message+self.message)
            self.edited = requests.post(url_editcomment)
            self.upvoted = requests.post(url_vote)
            
        else: 
            ban_message = '''This comment has been deleted for violating <a href="https://docs.google.com/document/d/1QXiKpWgGlhA75JNsPy8BltOdNahks61guas3zOQLpis/edit"><b><u>9Anime Comment Policy</u></b></a><br><br>You have been banned.<br><br>Username: @{}:disqus<br>Reason: {}<br>Banned By: {}<br>Your Comment: <spoiler>{}</spoiler>'''.format(self.user, self.reason, self.mod, self.message)
            
            url_post = 'https://disqus.com/api/3.0/posts/create.json?api_key={}&thread={}&access_token={}&message={}'.format(API_KEY,
                                                                                                                            6292105195,
                                                                                                                            access_token,
                                                                                                                            ban_message)
            self.posted = requests.post(url_post)
            
            print("Posted = {}".format(self.posted))
            
        url_ban_user = 'https://disqus.com/api/3.0/forums/block/banPostAuthor.json?api_key={}&post={}&access_token={}&notes={}&banEmail=1&banUser=1'.format(
                                                                                                                                 API_KEY,
                                                                                                                                 self.comment_id,
                                                                                                                                 access_token,
                                                                                                                                 ban_reason)
            
        self.deleted = requests.post(url_delete_comment)
        self.banned = requests.post(url_ban_user)

        print("Deleted = {}".format(self.deleted))
        print("Banned = {}".format(self.banned))
        
        self.send_alert_ban()
      

@app.route('/', methods=["POST", "GET"])
def login():

  if session.get('name'):
    return redirect(url_for('choice'))
  else:
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
  if session.get('name'):
    error = None
    if request.method == "POST":
        try:
          comment_id = int(request.form['comment_id'])

          url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY, comment_id, access_token)
          
          response = requests.get(url)
          response = json.loads(response.text)

          if response['response']['forum'] != '9anime-to':
            raise Exception

          return redirect(url_for('checkcomment', comment_id = comment_id))
        except Exception as e:
          print(e)
          error = "Invalid Comment ID"
          return render_template('viewcomment.html', error=error)
    return render_template("viewcomment.html")
  else:
    error = "Unauthorized Access."
    return render_template("login.html", error=error)


@app.route('/checkcomment/<int:comment_id>/', methods=["POST", "GET"])
def checkcomment(comment_id):
  if session.get('name'):
    try:

      if 'timeout_btn' in request.form:
        
        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY, comment_id, access_token)
            
        response = requests.get(url)
        response = json.loads(response.text)

        user_data = {
              'display_name':response['response']['author']['name'],
              'username':response['response']['author']['username'],
              'content':response['response']['message'].replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'),
              'upvotes':response['response']['likes'],
              'downvotes':response['response']['likes'],
            }

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{}') AND (TABLE_NAME = '{}')".format(app.config['MYSQL_DB'], user_data['username']))
        user = curl.fetchone()
        curl.close()

        user = user['count(*)']

        if user:
          curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          curl.execute("INSERT INTO {}(moderator, reason, permaban) VALUES ({}, {}, 0)".format(user_data['username'], session.get('name'), request.form['timeout_reason']))
          mysql.connection.commit()
          curl.close()
        else:
          curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          curl.execute("create table {}(id INT NOT NULL AUTO_INCREMENT, moderator VARCHAR(50) NOT NULL, reason VARCHAR(255) NOT NULL, permaban INT NOT NULL, log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id)))".format(user_data['username']))
          curl.execute("INSERT INTO {}(moderator, reason, permaban) VALUES ({}, {}, 0)".format(user_data['username'], session.get('name'), request.form['timeout_reason']))
          mysql.connection.commit()
          curl.close()
        
        discord_alert = DiscordAlert(comment_id, reason=request.form['timeout_reason'], timeout=request.form['timeout_duration'])
        discord_alert.timeout()

        success = "Timeout Issued"
        return render_template("comment.html", comment_id = comment_id, user_data = user_data, success=success)

      if 'ban_btn' in request.form:
        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY, comment_id, access_token)
            
        response = requests.get(url)
        response = json.loads(response.text)

        user_data = {
              'display_name':response['response']['author']['name'],
              'username':response['response']['author']['username'],
              'content':response['response']['message'].replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'),
              'upvotes':response['response']['likes'],
              'downvotes':response['response']['likes'],
            }
        
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{}') AND (TABLE_NAME = '{}')".format(app.config['MYSQL_DB'], user_data['username']))
        user = curl.fetchone()
        curl.close()

        user = user['count(*)']

        if user:
          curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          curl.execute("INSERT INTO {}(moderator, reason, permaban) VALUES ({}, {}, 1)".format(user_data['username'], session.get('name'), request.form['timeout_reason']))
          mysql.connection.commit()
          curl.close()
        else:
          curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
          curl.execute("create table {}(id INT NOT NULL AUTO_INCREMENT, moderator VARCHAR(50) NOT NULL, reason VARCHAR(255) NOT NULL, permaban INT NOT NULL, log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id)))".format(user_data['username']))
          curl.execute("INSERT INTO {}(moderator, reason, permaban) VALUES ({}, {}, 1)".format(user_data['username'], session.get('name'), request.form['timeout_reason']))
          mysql.connection.commit()
          curl.close()
        
        discord_alert = DiscordAlert(comment_id, reason=request.form['ban_reason'])
        discord_alert.ban()

        success = "Permanent Ban Issued"
        return render_template("comment.html", comment_id = comment_id, user_data = user_data, success=success)

      try:

        if request.method == "POST":
          comment_id = request.form['comment_id']
          comment_id = int(comment_id)

          url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY, comment_id, access_token)

          response = requests.get(url)
          response = json.loads(response.text)

          if response['response']['forum'] != '9anime-to':
            raise Exception

          return redirect(url_for('checkcomment', comment_id = comment_id))

      except Exception as e:
        error = "Invalid Comment ID"
        print(e)
        return render_template('viewcomment.html', error=error)

      comment_id = int(comment_id)

      url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}&access_token={}'.format(API_KEY, comment_id, access_token)
            
      response = requests.get(url)
      response = json.loads(response.text)

      if response['response']['forum'] != '9anime-to':
        return redirect(url_for('not_found'))

      user_data = {
              'display_name':response['response']['author']['name'],
              'username':response['response']['author']['username'],
              'content':response['response']['message'].replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>'),
              'upvotes':response['response']['likes'],
              'downvotes':response['response']['likes'],
            }
      
      curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      curl.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = '{}') AND (TABLE_NAME = '{}')".format(app.config['MYSQL_DB'], user_data['username']))
      user = curl.fetchone()
      curl.close()

      user = user['count(*)']

      if user:
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * from {} ORDER BY log_date DESC LIMIT 1".format(user_data['username']))
        user = curl.fetchone()
        curl.close()

        wait_period = (user['log_date'] + datetime.timedelta(days = 30))

        user['log_date'] = user['log_date'].strftime("%B %d, %Y")

        print(user)

        if (wait_period >= datetime.datetime.now()) or (user['permaban'] == 1):
          return render_template("comment.html", comment_id = comment_id, user_data = user_data, ban_info = user)
      else:
        return render_template("comment.html", comment_id = comment_id, user_data = user_data)

    except Exception as e:
      print(e)
      return redirect(url_for('not_found'))
  else:
    error = "Unauthorized Access."
    return render_template("login.html", error=error)


@app.route('/viewuser', methods=["POST", "GET"])
def viewuser():
  return "To be completed"


@app.route('/404')
def not_found():
  return render_template("404.html")


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")


if __name__ == '__main__':

  app.secret_key = 'lol'
  app.run(debug=True)