## Introduction
A bot written in Python, utilising Flask web frame and Disqus API to ease the moderation and logging for the 9Anime Disqus Moderator.

## Requirements
* flask >= 1.1.2
* flask-mysqldb >= 0.2.0
* discord-webhook >= 0.11.0
* yaml >= 0.2.5

## Login

The users are greeted with login screen prior upon starting the application. The login screen looks like below.

![Login Screen](https://github.com/KennyStryker/9anime-disqus-bot/blob/main/images/loginscreen.png?raw=true)

The login system utilizes MySQL to authenticate the moderators.

## User Choice

Upon login, the moderators are given two choices, **Check Comment** and **Check User**, as shown below.

![Choice Screen](https://github.com/KennyStryker/9anime-disqus-bot/blob/main/images/choice.png?raw=true)

## Check Comment

Upon clicking **Check Comment**, you'll be introduced to the following screen where you'll be asked to enter the comment id.

![Comment Screen](https://github.com/KennyStryker/9anime-disqus-bot/blob/main/images/comment.png?raw=true)

The users can either input **comment ID** or **comment URL** to retrieve the information regarding the comment and poster.

Upon entry, the Disqus API will fetch information regarding the comment, like author, content, upvotes, downvotes, etc, as shown below.

![Comment Fetch](https://github.com/KennyStryker/9anime-disqus-bot/blob/main/images/viewcomment.png?raw=true)