from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from database.AreaTypes import AreaTypes
from Helpers.bools import BoolFromInt
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
    life = Column(Integer, nullable=False)
    location = Column(Integer, nullable=False)
    current_area = Column(Integer, ForeignKey('area.area_id'), nullable=False)

    def __repr__(self):
        if self.alive == 1:
            return f"Name: {self.name}\n ID: {self.id} \n Class: {self.klasse} \n Race: {self.race} \n Level: {self.level} \n Life: {self.life} \n"
        else:
            return f"{self.name} is Dead"

    def take_damage(self, value):
        self.life = self.life - value
        if self.life <= 0:
            self.alive = 0
            return f"{self.name} died from the wounds"
        return None

    def get_location(self):
        return self.location

    def get_area(self):
        return self.current_area

    def move_to_area(self, areaid):
        self.current_area = areaid


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable=False)
    discord_id = Column(String, nullable=False)
    user_type_id = Column(Integer, ForeignKey('user_type.id'))
    #user_type = relationship("UserTypes", back_populates='')
    character_id = Column(Integer, ForeignKey('characters.id'))
    def __repr__(self):
        return f"{self.name} | {self.id}"


class UserCharater(Base):
    __tablename__ = 'user_characters'
    user_character_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
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

class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    name = Column(String)
    item_id = Column(Integer, ForeignKey('item.item_id'))
    loottable = Column(Integer)

class Item(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    item_type = Column(String, nullable=False)
    rarity = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    base_armor = Column(Integer)
    base_damage = Column(Integer)
    rarity_levels = 7
    def __repr__(self):
        for i in range(0, rarity_levels):
            if i == self.rarity and i == 1:
                rarity_value = 'Common'
            elif i == self.rarity and i == 2:
                rarity_value = 'Uncommon'
            
            elif i == self.rarity and i == 3:
                rarity_value = 'Rare'
            
            elif i == self.rarity and i == 4:
                rarity_value = 'Unique'
            
            elif i == self.rarity and i == 5:
                rarity_value = 'Legendary'
            
            elif i == self.rarity and i == 6:
                rarity_value = 'Artifact'
            
            elif i == self.rarity and i == 7:
                rarity_value = 'Quest'
            else:
                rarity_value = 'Unknown'

        return f"\n{self.item_id}\n{self.name}\n{self.description}\n{self.item_type}\n{self.rarity}"

class Creature(Base):
    __tablename__ = 'creature'
    creature_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    level = Column(Integer, nullable=False)
    experience = Column(Integer)
    inventory = Column(Integer, ForeignKey('inventory.inventory_id'))
    klasse = Column(String, nullable=False)
    race = Column(String, nullable=False)
    life = Column(Integer, nullable=False)
    location = Column(Integer, nullable=False)
    area = Column(Integer, ForeignKey('area.area_id'), nullable=False)

class Area(Base):
    __tablename__ = 'area'
    area_id = Column(Integer, primary_key=True)
    area_type = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"Area {self.name} has ID {self.area_id} and is of type {self.area_type}"


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
        Area(area_type=2, name='The Wild'),
        Area(area_type=1, name="Haven"),
        Inventory(name="Zombie Loottable", loottable=1),
        Creature(name='Zombie', level=1, experience=3, inventory=1, klasse="Undead Brute", race="Undead", life=30, location=3, area=1)
    ])

def get_character_attributes(session, c_id = None):
    if c_id == None:
        for res, test in session.query(Character_Attribute, Character).join(Character).filter(Character.id == Character_Attribute.character_id).all():
           for res2 in session.query(Attribute).filter(Attribute.id == res.attribute_id).all():
               print(f"{test.name} has {res.value} in {res2.name}")
               return f"{test.name} has {res.value} in {res2.name}"
    else:
        for res, test in session.query(Character_Attribute, Character).join(Character).filter(Character.id == c_id).all():
           for res2 in session.query(Attribute).filter(Attribute.id == res.attribute_id).all():
               print(f"{test.name} has {res.value} in {res2.name}")
               return f"{test.name} has {res.value} in {res2.name}"

def get_target_by_name(session, target_name):
    res = session.query(Character).filter(Character.name == target_name).one_or_none()
    print(f"From DB.py {res}")
    return res

def change_character_by_name(session, character, property, value):
    try:
        Character.update().where(Character.name == character).\
            values(property = value)
        return True
    except:
        raise

def get_all_areas(session):
    try:
        return session.query(Area).all()
    except:
        return None

def get_character_by_discord(session, username):
    char = session.query(User).filter(User.discord_id == username).one_or_none()
    return char