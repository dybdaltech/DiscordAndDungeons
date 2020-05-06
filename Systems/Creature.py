from database.db import Creature 

class CCreature:
    def __init__(self, name, level, experience, inventory, klasse, race, life, location, area):
        self.name = name
        self.level = level
        self.experience = experience
        self.inventory = inventory
        self.klasse = klasse
        self.race = race
        self.life = life
        self.location = location
        self.area = area
        self.armor = 10
        self.actions = []

    def save(self):
        cr = Creature(name=self.name, level=self.level, experience=self.experience, inventory=self.inventory, klasse=self.klasse, race=self.race, life=self.life, location=self.location, area=self.area, armor=self.armor)
        session.save(self)
