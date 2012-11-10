""" teaming.py  team members

"""
from myapp.helps.toting import Tote

class Player(Tote):
    """ """
    Keys =  ['name', 'kind', 'strength', 'speed', 'health',  'attack', 'defend']
    def __init__(self, name="", kind="good",strength=2, speed=2, health=10,
                 attack=2, defend=2):
        """ """
        self.name = name.strip().replace(" ", '')
        self.kind = kind
        self.strength = strength
        self.speed = speed
        self.health = health
        self.attack =  attack
        self.defend = defend
    

class Team(Tote):
    """   """
    def __init__(self, name="", players=None):
        self.name = name.strip().replace(" ", '')
        self.players = dict(players or {}) #make copy
        
    def addPlayer(self, player):
        """ """
        if not self.players.get(player.name, None):
            self.players[player.name] = player
        return self
    
    def replacePlayer(self, player):
        """ """
        self.players[player.name] = player
        return self
    
    def removePlayer(self, player=None,  name=""):
        """ """
        player = self.players.get(player.name if player else name)
        if player:
            del  self.players[player.name]
        return self


teams = {}
team = Team(name="Red")
for x in [ dict(name="John"),  dict(name="Betty"), dict(name="Rich"),
           dict(name="Susan"), ]:
    team.addPlayer(Player(**x))

teams[team.name] = team

team = Team(name="Blue")
for x in [ dict(name="Peter"),  dict(name="Jenny"), dict(name="Jack"),
           dict(name="Trish"), ]:
    team.addPlayer(Player(**x))

teams[team.name] = team