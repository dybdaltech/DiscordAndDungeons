from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
Base = declarative_base()

eng = create_engine('sqlite:///data.db')

# User connects to a Discord Guild, add user to DB, when user types !start (or start command)
# The user follows through a form, example:
# Character name: !a <name>
# Character Class: !a <class> (or type !h classes to list classes)
# Character Race: !a <race> !h races
# The user then gains the UserType 3 tag (update where DiscordID == discord_id) set user_type_id = 3.
# https://github.com/jgoodman/MySQL-RPG-Schema/blob/master/create_tables.sql

class UserTypes(Base):
    __tablename__ = 'user_type'
    id = Column(Integer, primary_key = True)
    name = Column(String)
#Usertypes:
#1 = Administrator
#2 = GameMaster
#3 = Player
#4 = Non-player (before character creation)


    
class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    alive = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    inventory = Column(Integer)
    klasse = Column(String, nullable=False)
    race = Column(String, nullable=False)

    def __repr__(self):
        return f"{self.name} | {self.id} | {self.klasse} | {self.race}"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable=False, unique=True)
    discord_id = Column(String, nullable=False, unique=True)
    user_type_id = Column(Integer, ForeignKey('user_type.id'))
    #user_type = relationship("UserTypes", back_populates='')
    character_id = Column(Integer, ForeignKey('characters.id'))
    def __repr__(self):
        return f"{self.name} | {self.id}"


class UserCharater(Base):
    __tablename__ = 'user_characters'
    user_character_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    character_id = Column(Integer, ForeignKey('characters.id'))
    
    def __repr__(self):
        return f"<{self.user_character_id}> | <{self.user_id}> | <{self.character_id}>"

class Attribute(Base):
    __tablename__ = 'attribute'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    def __repr__(self):
        return f"{self.name} | {self.description} | {self.id}"

class Character_Attribute(Base):
    __tablename__ = 'character_attributes'
    character_attribute_id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    attribute_id = Column(Integer, ForeignKey('attribute.id'))
    value = Column(Integer, nullable = False)

    def __repr__(self):
        return f"{self.character_id} | {self.attribute_id} | {self.value} "

Session = sessionmaker(bind=eng)
session = Session()
Base.metadata.create_all(eng)

def preload(session, base):
    base.metadata.create_all(eng)
    session.add_all([
        UserTypes(name="Administrator"),
        UserTypes(name="GameMaster"),
        UserTypes(name="Player"),
        UserTypes(name="Non-player"),
        Attribute(name="Strength", description="Measures how physically strong you are."),
        Attribute(name="Dexterity", description="A measure of your agility and reflexes."),
        Attribute(name="Intelligence", description="How mentally strong and smart you are."),
    ])

def get_character_attributes(session, c_id = None):
    if c_id == None:
        for res, test in session.query(Character_Attribute, Character).join(Character).filter(Character.id == Character_Attribute.character_id).all():
           for res2 in session.query(Attribute).filter(Attribute.id == res.attribute_id).all():
               print(f"{test.name} has {res.value} in {res2.name}")
    else:
        for res, test in session.query(Character_Attribute, Character).join(Character).filter(Character.id == c_id).all():
           for res2 in session.query(Attribute).filter(Attribute.id == res.attribute_id).all():
               print(f"{test.name} has {res.value} in {res2.name}")

