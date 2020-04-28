import random

class Action(object):
    def __init__(self, _name, _type, _stat, _user):
        self.name = _name
        self.type = _type
        self.stat = _stat
        self.user = _user

    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Action {self.name}, {self.type}, {self.stat} | {self.user}"

def PhysicalAction(Action):
    def __init__(self, name, user):
        super().__init__(name, 'physical', 'strength', user)
    def use(self, target):
        damage = (random.randint(self.user.strength, self.user.strength*2)) - target['armor']
        target.take_damage(damage)
    
    def desc(self):
        return f"{self.name}: {self.user['name']}"

    def __repr__(self):
        return f"Physical Action {self.name}"
    
def MagicAction(Action):
    def __init__(self, name, user):
        super().__init__(name, 'Magical', 'Intelligence', user)

    def use(self, target):
        self.user

    def desc(self):
        return f"{self.name}: {self.user['name']}"

    def __repr__(self):
        return f"Magical Action {self.name}"
    
    