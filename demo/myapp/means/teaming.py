""" teaming.py  team members

"""
from collections import OrderedDict as ODict

nextTID = 1
nextPID = 1


DEFAULT_PLAYER = ODict([('id', None), ('tid', None), ('name', ""),
                        ('kind', "good"), ('strength', 2),('speed', 2),
                        ('health', 5), ('attack', 3), ('defend', 4)])
DEFAULT_TEAM =  ODict([('id', None), ('name', ""), ('players', None)])

def newTeam(name=""):
    global nextTID
    
    team = ODict(DEFAULT_TEAM) #make copy
    team['id'] = nextTID
    nextTID += 1
    if name:
        team['name'] = name
    team['players'] = ODict()
    return team

def newPlayer(name = "", team=None):
    global nextPID
    
    player = ODict(DEFAULT_PLAYER) #make copy
    player['id'] = nextPID
    nextPID += 1
    if name:
        player['name'] =  name    
    if team:
        player['tid'] = team["id"]
    
    return player
        

init = [
        ("red", ("John",  "Betty", "Rich", "Susan")),
        ("blue", ("Peter", "Jenny", "Jack", "Trish")), 
       ]

teams = ODict()
players = ODict()


for tname, pnames in init:
    team = newTeam(name=tname)
    teams[team['id']] = team
    for pname in pnames:
        player = newPlayer(name=pname, team=team)
        players[player['id']] = player
        team['players'][player['id']] = player

if __name__ == "__main__":
    """Process command line args """
    print "Teams:"
    for tid, team in teams.items():
        print tid, team
    
    print "Players:"
    for pid, player in players.items():
        print pid, player