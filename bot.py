# bot.py

import os
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intent = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intent)


def load_sniper_data():
    try:
        with open('sniper_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save sniper data to a file


def save_sniper_data(data):
    with open('sniper_data.json', 'w') as file:
        json.dump(data, file)


# Function to load target data from a file

def load_target_data():
    try:
        with open('target_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save target data to a file


def save_target_data(data):
    with open('target_data.json', 'w') as file:
        json.dump(data, file)


@bot.event
async def on_ready():
    global target_count
    global sniper_count
    sniper_count = load_sniper_data()
    target_count = load_target_data()
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def snipe(ctx, *, user_mention: discord.Member = None):
    global sniper_count
    global target_count
    has_image = False

    if len(ctx.message.attachments) > 0:
        for attachment in ctx.message.attachments:
            if attachment.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                has_image = True

    if True and user_mention:

        sniper_id = ctx.message.author.id
        # Update the sniper count for the mentioned user
        if sniper_id not in target_count:
            sniper_count[sniper_id] = 1
        else:
            sniper_count[sniper_id] += 1

        # Update the target count for the mentioned user
        if user_mention.id not in target_count:
            target_count[user_mention.id] = 1
        else:
            target_count[user_mention.id] += 1

        await ctx.send(f"{ctx.author.mention} just sniped {user_mention.mention}!")

        # Save snipe data to a file after each snipe
        print(user_mention.id)
        save_target_data(target_count)
        save_sniper_data(sniper_count)

    else:
        await ctx.send("Please use the command with a mention and an image attachment.")


@bot.command()
async def reset(ctx):
    if os.path.exists('target_data.json'):
        os.remove('target_data.json')
    if os.path.exists('sniper_data.json'):
        os.remove('sniper_data.json')
    global target_count
    global sniper_count
    target_count = load_target_data()
    sniper_count = load_sniper_data()
    await ctx.send(f"Leaderboard has been reset!")


@bot.command()
async def leaderboard(ctx):
    global target_count
    global sniper_count
    target_count = load_target_data()
    sniper_count = load_sniper_data()
    # Sort the snipe count dictionary by value (number of snipes)
    sorted_targets = sorted(target_count.items(),
                            key=lambda x: x[1], reverse=True)
    sorted_snipers = sorted(sniper_count.items(),
                            key=lambda x: x[1], reverse=True)

    target_leaderboard = "\n".join(
        f"{bot.get_user(int(user)).mention}: {count} snipes" for user, count in sorted_targets)
    await ctx.send(f"Most Sniped:\n{target_leaderboard}")
    sniper_leaderboard = "\n".join(
        f"{bot.get_user(int(user)).mention}: {count} snipes" for user, count in sorted_snipers)
    await ctx.send(f"Top Snipers:\n{sniper_leaderboard}")


bot.run(TOKEN)
