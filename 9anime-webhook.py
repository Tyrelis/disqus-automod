from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/808249420750520351/7S3GqGkalYuzmNi8M9x6dU3KGjeR40sTbVv0d4ROSwtO_HbrjpBItAuiKfAtCMHtoEuI')

embed = DiscordEmbed(title='Timeout Issued',
                    description='Test description',
                    color=242424)

webhook.add_embed(embed)

response = webhook.execute()