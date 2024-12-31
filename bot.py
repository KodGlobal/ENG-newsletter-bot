import discord
from discord.ext import commands, tasks
import feedparser
from config import TOKEN

# Create an intents object for the bot so that the bot can receive messages
intents = discord.Intents.default()
intents.messages = True

# Create a bot object with the '!' prefix for commands
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionaries to store subscriptions and news
subscriptions = {}
news_cache = {}

# Predefined RSS feed URL
rss_feed_url = "https://www.cbc.ca/webfeed/rss/rss-world"

# Function to get news from the RSS feed
def get_news(feed_url):
    feed = feedparser.parse(feed_url)
    return [{'title': entry.title, 'link': entry.link} for entry in feed.entries]

# Command to show news from a predefined source
@bot.command()
async def news(ctx):
    news = get_news(rss_feed_url)
    if not news:
        await ctx.send("Failed to retrieve news from the specified source.")
        return
    response = "\n".join([f"{entry['title']} - {entry['link']}" for entry in news[:5]])
    if response:
        await ctx.send(response)
    else:
        await ctx.send("No available news.")

# Command to subscribe to notifications by keyword
@bot.command()
async def subscribe(ctx, keyword):
    user_id = ctx.author.id
    if user_id not in subscriptions:
        subscriptions[user_id] = []
    if keyword not in subscriptions[user_id]:
        subscriptions[user_id].append(keyword)
        await ctx.send(f"You have subscribed to notifications for the keyword: {keyword}")
    else:
        await ctx.send(f"You are already subscribed to notifications for the keyword: {keyword}")

# Command to unsubscribe from notifications by keyword
@bot.command()
async def unsubscribe(ctx, keyword):
    user_id = ctx.author.id
    if user_id in subscriptions and keyword in subscriptions[user_id]:
        subscriptions[user_id].remove(keyword)
        await ctx.send(f"You have unsubscribed from notifications for the keyword: {keyword}")
    else:
        await ctx.send(f"You are not subscribed to notifications for the keyword: {keyword}")

# Command to show current subscriptions
@bot.command()
async def notifications(ctx):
    user_id = ctx.author.id
    if user_id in subscriptions and subscriptions[user_id]:
        response = "You are subscribed to the following keywords:\n" + "\n".join(subscriptions[user_id])
    else:
        response = "You are not subscribed to any keywords."
    await ctx.send(response)

# Command to show the latest news for all subscriptions
@bot.command()
async def latest(ctx):
    user_id = ctx.author.id
    if user_id in subscriptions and subscriptions[user_id]:
        user_news = []
        for keyword in subscriptions[user_id]:
            if keyword in news_cache:
                user_news.extend(news_cache[keyword])
        response = "\n".join([f"{entry['title']} - {entry['link']}" for entry in user_news[:5]])
        if response:
            await ctx.send(response)
        else:
            await ctx.send("No news for your subscriptions.")
    else:
        await ctx.send("No news for your subscriptions.")

# Background task to update news every 10 minutes
@tasks.loop(minutes=10)
async def update_news():
    news = get_news(rss_feed_url)
    for entry in news:
        for keyword in subscriptions.values():
            if any(word.lower() in entry['title'].lower() for word in keyword):
                if keyword not in news_cache:
                    news_cache[keyword] = []
                news_cache[keyword].append(entry)

# Command to display information about available commands
@bot.command()
async def info(ctx):
    response = (
        "Available commands:\n"
        "!news - show the latest news from the specified source.\n"
        "!subscribe <keyword> - subscribe to notifications for a keyword.\n"
        "!unsubscribe <keyword> - unsubscribe from notifications for a keyword.\n"
        "!notifications - show current subscriptions.\n"
        "!latest - show the latest news for all subscriptions.\n"
        "!info - display this help information."
    )
    await ctx.send(response)

# Start the background task when the bot starts
@bot.event
async def on_ready():
    update_news.start()
    print(f'Logged in as {bot.user}')

# Run the bot with the token from config.py
bot.run(TOKEN)
