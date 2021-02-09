from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808249420750520351/7S3GqGkalYuzmNi8M9x6dU3KGjeR40sTbVv0d4ROSwtO_HbrjpBItAuiKfAtCMHtoEuI')

API_KEY = 'nl55taKAfLJah7i8EaglOrFEoifCONO9SwOno5DiNanv0FPXwlxufjQ7DIP3drhc'

class DiscordAlert:
    def __init__(self, comment_id):

        global API_KEY

        url = 'https://disqus.com/api/3.0/posts/details.json?api_key={}&post={}'.format(API_KEY, comment_id)
        
        response = requests.get(url)
        response = json.loads(response.text)
        
        self.user = response['response']['author']['username']
        self.comment_id = id
        self.timeout_duration = "1 Days"
        self.mod = "Kenny Senpai"
        self.comment_url = 'https://9anime-to.disqus.com/admin/moderate/pending/search/id:{}'.format(comment_id)

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