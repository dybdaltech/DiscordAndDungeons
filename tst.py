import discord, yaml
from discord.ext import commands
#from database import db

config_file = open(r'./config.yml')
cfg = yaml.full_load(config_file)

bot = commands.Bot(command_prefix="!", description = "Test")
#def add_character(session):
#    cname = input("Character name: ")
#    calive = 1
#    clevel = 1
#    cexperience = 1
#
#    uname = input("Username: ")
#    udiscord = input("Discord ID: ")
#    utype = 1
#    session.add_all([
#        db.User(name=uname, discord_id=udiscord, user_type_id=utype),
#        db.Character(name= cname, alive = calive, level = clevel, experience = cexperience)
#    ])
#
#db.preload(db.session, db.Base)
#add_character(db.session)
#for ch in db.session.query(db.Character).all():
#    print(ch)
#
#
initial_extensions = ['cogs.character']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}\nVersion {discord.__version__}\n")

bot.run(cfg["discord_token"], bot=True)

#https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
#https://docs.sqlalchemy.org/en/13/core/metadata.html
#https://github.com/Naatoo/pygame-RPG2d/tree/develop/src/database