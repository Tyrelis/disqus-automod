from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808249420750520351/7S3GqGkalYuzmNi8M9x6dU3KGjeR40sTbVv0d4ROSwtO_HbrjpBItAuiKfAtCMHtoEuI')

user = "Kenny"
comment_id = "4225445"
timeout_duration = "3 Days"
mod = "Kenny Stryker"
comment_url = "https://www.undefined.com"

embed = DiscordEmbed(title='Timeout Issued',
                    color=0x5A2E98)

embed.set_author(name="View Comment", url=comment_url)

embed.add_embed_field(name="User", value=user)
embed.add_embed_field(name="Comment ID", value=comment_id)
embed.add_embed_field(name="Timeout Duration", value=timeout_duration)
embed.add_embed_field(name="Moderator", value=mod)

webhook.add_embed(embed)
response = webhook.execute()