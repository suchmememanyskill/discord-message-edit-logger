import discord, os, logging

intents = discord.Intents.none()
intents.members = True
intents.message_content = True
intents.guild_messages = True

TOKEN = os.environ['BOT_TOKEN']

BOT_LISTEN_CHANNEL_IDS = os.environ['BOT_LISTEN_CHANNEL_IDS']

if BOT_LISTEN_CHANNEL_IDS == '*':
    CHANNEL_IDS = []
    ALL_CHANNEL_IDS = True
else:
    CHANNEL_IDS = [int(x.strip()) for x in BOT_LISTEN_CHANNEL_IDS.split(";")]
    ALL_CHANNEL_IDS = False

LOG_DELETED_CHANNEL_ID = os.getenv('LOG_DELETED_CHANNEL_ID', '')
LOG_EDITED_CHANNEL_ID = os.getenv('LOG_EDITED_CHANNEL_ID', '')

logger = logging.getLogger('discord.bot')
bot = discord.Client(intents=intents)

async def get_channel(id : int|str):
    id = int(id)

    channel = bot.get_channel(id)

    if not channel:
        channel = await bot.fetch_channel(id)
    
    return channel

@bot.event
async def on_message_delete(message : discord.Message):
    if (not LOG_DELETED_CHANNEL_ID) or ((not ALL_CHANNEL_IDS) and message.channel.id not in CHANNEL_IDS):
        logger.info("Ignored deleted message")
        return

    embed = discord.Embed(title="Message deleted", description=message.content, color=discord.Colour.red())
    embed.set_footer(icon_url=message.author.avatar.url, text=f"{message.author.name} | {message.author.id}")
    channel = await get_channel(LOG_DELETED_CHANNEL_ID) 
    await channel.send(embed=embed)

@bot.event
async def on_message_edit(before : discord.Message, after : discord.Message):
    if (not LOG_EDITED_CHANNEL_ID) or ((not ALL_CHANNEL_IDS) and before.channel.id not in CHANNEL_IDS):
        logger.info("Ignored edited message")
        return

    embed = discord.Embed(title="Message edited", color=discord.Colour.orange())
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    embed.set_footer(icon_url=before.author.avatar.url, text=f"{before.author.name} | {before.author.id}")
    channel = await get_channel(LOG_EDITED_CHANNEL_ID) 
    await channel.send(embed=embed)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info('------')

bot.run(TOKEN)
