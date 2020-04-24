import discord
from discord.ext import commands, flags
from database import db

class Character(commands.Cog):
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session


    @commands.command(name="greet")
    async def greet(self, ctx):
        print(ctx.message.author)
        await ctx.send(f"Hello! My name is {self.Character}")

    @flags.add_flag("-name")
    @flags.add_flag("-klasse")
    @flags.add_flag("-race")
    @flags.command(name="newplayer")
    async def NewPlayer(self, ctx, **flags):
        uname = ctx.message.author
        udiscord = ctx.message.author
        utype = 1
        cname = "{name!r}".format(**flags)
        calive = 1
        clevel = 1
        cexperience = 1
        cclass = "{klasse!r}".format(**flags)
        crace = "{race!r}".format(**flags)
        print(uname, udiscord, utype, cname, cclass, crace)
        try:
            self.session.add_all([
                db.User(name=str(uname), discord_id=str(udiscord), user_type_id=utype),
                db.Character(name= cname, alive = calive, level = clevel, experience = cexperience, klasse=cclass, race=crace)
            ])
            self.session.commit()
        except:
            self.session.rollback()
            raise
        await ctx.send(content=f"Welcome {cname} to the dungeon of discord!")
    @commands.command(name="embed")
    async def example_embed(self, ctx):
        """Shows latest info"""

        embed = discord.Embed(title=self.Character,
            description='An showcase of the bots ability to embed')
        embed.set_author(name = Character, url="https://github.com/dybdaltech/DiscordAndDungeons")
        await ctx.send(content='', embed=embed)
    
    @commands.command(name="get_all_characters")
    async def GetAllCharacters(self, ctx):
        result = []
        try:
            for res in self.session.query(db.Character).all():
                result.append(res)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        await ctx.send(content=result)


db.preload(db.session, db.Base)
def setup(bot):
    bot.add_cog(Character(bot, db.session))