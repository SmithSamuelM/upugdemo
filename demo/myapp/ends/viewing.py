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

@app.route('/backend/teams/') 
@app.route('/backend/teams') #angular strips trailing slash if no <name>
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

@app.route('/backend/teams/<name>') #angular strips trailing slash if no <name>
def teamsNameGet(name):
    team = teaming.teams.get(name, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % name)
    return team


@app.get('/backend/team/<tname>/player/')
@app.get('/backend/team/<tname>/player')
def teamPlayersGet(tname):
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    players = []
    name = bottle.request.query.get('name', '')
    if name: #return list of the one player that matches query
        player = teaming.teams.get(tname).get('players').get(name)
        if not player:
            bottle.abort(404, "Player '%s' not found." % name)
        players.append(player) #return list with the one player that matches query    
    else:
        for player in team['players'].values():
            players.append(player)
    
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(players) 

@app.get('/backend/team/<tname>/player/<name>') 
def teamPlayerGet(tname, name):
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    player = team['players'].get(name, None)
    if not player:
        bottle.abort(404, "Player '%s' on team '%s' not found." % (name, tname))    
    return player

@app.get('/backend/team/<tname>/player/<name>/put') #testing only
@app.post('/backend/team/<tname>/player/<name>') 
@app.put('/backend/team/<tname>/player/<name>') 
def teamPlayerPut(tname, name):
    data = bottle.request.json
    if not data:
        bottle.abort(400, "Empty order data in request body.")
        
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    
    if data.get('name') and name != data['name']:
        bottle.abort(400, "Url player name '%s' does not match request body name '%s'."
                     % (name, data['name']))
        
    player = team['players'].get(name, None)
    if not player: #new player
        player = teaming.DEFAULT_PLAYER
        team['players'][name] = player
    
    player.update(data)
    
    return player

@app.get('/backend/team/<tname>/player/<name>/del') #testing only
@app.delete('/backend/team/<tname>/player/<name>') 
def teamPlayerDelete(tname, name):
    team = teaming.teams.get(tname, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tname)
    
    player = team['players'].get(name, None)
    if not player: #new player
        bottle.abort(404, "Player '%s' on team '%s' not found." % (name, tname))  
    
    del team['players'][name]
    
    return {}
