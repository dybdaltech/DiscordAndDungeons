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
        clife = 100
        cclass = "{klasse!r}".format(**flags)
        crace = "{race!r}".format(**flags)
        print(uname, udiscord, utype, cname, cclass, crace)
        try:
            self.session.add_all([
                db.User(name=str(uname), discord_id=str(udiscord), user_type_id=utype),
                db.Character(name= cname, alive = calive, level = clevel, experience = cexperience, klasse=cclass, race=crace, life=clife, location=1000, current_area=2)
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

    @flags.add_flag("-target")
    @flags.command(name="attack")
    async def character_attack(self, ctx, **flags):
        target = "{target!r}".format(**flags)
        #Query DB for a possible target within range
        try:
            target = db.get_target_by_name(self.session, target)
            if target == None:
                await ctx.send(content="Target not found!")
            else:
                atk = target.take_damage(10)
                if atk != None:
                    await ctx.send(content=atk)
                else:
                    await ctx.send(content=target)
            self.session.commit()
        except:
            await ctx.send(content="Error targetting")
            self.session.rollback()
            raise
    @flags.add_flag('-all')
    @flags.command(name="area")
    async def get_available_areas(self, ctx, **flags):
        #target = "{target!r}".format(**flags)
        #Query DB for a possible target within range
        try:
            areas = db.get_all_areas(self.session)
            await ctx.send(content=str(areas))
        except:
            await ctx.send(content="Error getting areas, check logs")


    @flags.add_flag('-destination', alias='-d')
    @flags.command(name='move')
    async def move_to_area(self, ctx, **flags):
        #Get who sent command from ctx.message.author
        #Find character based on who sent the command
        #Move the character from current area to new area. 
        udiscord = ctx.message.author
        destination = "{destination!r}".format(**flags)
        character_to_move = db.get_character_by_discord(self.session, udiscord)
        try:
            character_to_move.move_to_area(destination)
            await ctx.send(content=f"")
        except:
            await ctx.send(content="Error moving to area")

db.preload(db.session, db.Base)
def setup(bot):
    bot.add_cog(Character(bot, db.session))