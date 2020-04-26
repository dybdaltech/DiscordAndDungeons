#this should handle NPC creation and keep track of them

class NPC_Manager:
    def __init__(self, nid, faction, session, max_npc = 10):
        self.nid = nid
        self.session = session
        self.faction = faction
        self.max_npc = max_npc 

    def start(self):
        for i in range(0, self.max_npc):
            pass
        pass