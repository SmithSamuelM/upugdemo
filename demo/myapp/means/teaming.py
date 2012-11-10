""" teaming.py  team members

"""

DEFAULT_PLAYER = dict(name="", kind="good", strength=2, speed=2, health=5, attack=3, defend=4 )
teams = {}
team = dict(name="Red", players=dict())
for x in [ dict(name="John"),  dict(name="Betty"), dict(name="Rich"),
           dict(name="Susan"), ]:
    player = dict(DEFAULT_PLAYER)
    player.update(x)
    team['players'][player['name']] = player

teams[team['name']] = team

team = dict(name="Blue", players=dict())
for x in [ dict(name="Peter"),  dict(name="Jenny"), dict(name="Jack"),
           dict(name="Trish"), ]:
    player = dict(DEFAULT_PLAYER)
    player.update(x)
    team['players'][player['name']] = player

teams[team['name']] = team


