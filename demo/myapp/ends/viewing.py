""" Rest endpoints
    
"""
import json

import bottle
import myapp
from myapp.means import teaming

app = myapp.app #get app from myapp package.

@app.route('/backend/test') 
def testGet():
    return dict(result='success')

@app.route('/backend/teams') 
def teamsGet():
    teams =  []
    name = bottle.request.query.get('name', '')
    if name: #return list of the one team that matches query
       team = teaming.teams.get(name)
       if not team:
            bottle.abort(404, "Team '%s' not found." % name)
       teams.append(team) #return list with the one team that matches query
    else: #return list of all teams
        for team in teaming.teams.values():
            teams.append(team)
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(teams) 

@app.route('/backend/teams/<name>') 
def teamsNameGet(name):
    team = teaming.teams.get(name, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % name)
    return team


@app.route('/backend/team/<name>/players') 
def teamPlayersGet(name):
    team = teaming.teams.get(name, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    players = []
    for player in team['players'].values():
        players.append(player)
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(players) 

@app.route('/backend/team/<tname>/player/<name>') 
def teamPlayerGet(tname, name):
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    player = team['players'].get(name, None)
    if not player:
        bottle.abort(404, "Player '%s' on team '%s' not found." % (name, tname))    
    return player

@app.route('/backend/team/<tname>/player/<name>/put')
@app.route('/backend/team/<tname>/player/<name>', method='PUT') 
def teamPlayerPut(tname, name):
    data = bottle.request.json
    if not data:
        bottle.abort(400, "Empty order data in PUT body.")
        
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    
    player = team['players'].get(name, None)
    if not player: #new player
        player = teaming.DEFAULT_PLAYER
        team['players'] = player
    
    player.update(data)
    
    return player

@app.route('/backend/team/<tname>/player/<name>/del')
@app.route('/backend/team/<tname>/player/<name>', method='DELETE') 
def teamPlayerDelete(tname, name):
    data = bottle.request.json
    if not data:
        bottle.abort(400, "Empty order data in PUT body.")
        
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    
    player = team['players'].get(name, None)
    if not player: #new player
        bottle.abort(404, "Player '%s' on team '%s' not found." % (name, tname))  
    
    del team['players'][name]
    
    return {}
