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

@app.route('/backend/teams') #angular strips trailing slash if no <tid>
def teamsGet():
    
    name = bottle.request.query.get('name', '')
    teams =  []
    for team in teaming.teams.values():
        if name: #return list of the teams that matches query
            if team['name'] == name: 
               teams.append(team)
        else: #return list of all teams
            teams.append(team)
            
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(teams) 

@app.route('/backend/teams/<tid>') #angular strips trailing slash if no <name>
def teamIdGet(tid):
    try:
        tid = int(tid)
    except ValueError:
        bottle.abort(400, "Invalid team id %s" % tid)
        
    team = teaming.teams.get(tid, None)
    if not team:
        bottle.abort(404, "Team '%s' not found." % tid)
    return team

@app.get('/backend/players') #angular strips trailing slash if no <pid>
def playersGet():
    name = bottle.request.query.get('name', '')
    players = []
    for player in teaming.players.values():
        if name: #return list of the players that matches query
            if player['name'] == name: 
               players.append(player)
        else: #return list of all teams
            players.append(player)
    
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(players) 

@app.get('/backend/players/<pid>') 
def playerIdGet(pid):
    try:
        pid = int(pid)
    except ValueError:
        bottle.abort(400, "Invalid player id %s" % pid)    
    
    player = teaming.players.get(pid, None)
    if not player:
        bottle.abort(404, "Player '%s' not found." % (pid,))    
    return player

@app.get('/backend/players/create/create') #testing only
@app.post('/backend/players') 
def playerIdPost():
    """Create player"""     
    data = bottle.request.json
    if not data:
        bottle.abort(400, "Empty order data in request body.")
    
    name = data.get('name')
    if not name:
        bottle.abort(400, "Name required.")
    
    try:
        tid = int(data.get('tid'))
    except ValueError, TypeError:
        tid = None
        data['tid'] = None
    team = teaming.teams.get(tid) if tid else None
    
    player = newPlayer(name = name, team=team)
    for key, val in data.items():
        if key in player: #only change exiting fields
            player[key] = val
    if team:
        team['players'][player['id']] = player
    
    return player

@app.get('/backend/players/<pid>/update') #testing only
@app.put('/backend/players/<pid>') 
def playerIdPut(pid):
    """Update player"""
    try:
        pid = int(pid)
    except ValueError:
        bottle.abort(400, "Invalid player id %s" % pid)      
    player = teaming.players.get(pid, None)
    if not player:
        bottle.abort(404, "Player '%s' not found." % (pid,))     
    data = bottle.request.json
    if not data:
        bottle.abort(400, "Empty order data in request body.")
    
    dpid = data.get('id')
    if dpid and  dpid != pid:
        bottle.abort(400, "ID in request body not match ID in url.")
        
    name = data.get('name')
    if not name:
        bottle.abort(400, "Name required.")
    
    newTid = int(data.get('tid')) if data.get('tid') else None
    newTeam = teaming.teams.get(newTid)
    
    oldTid = int(player.get('tid')) if player.get('tid') else None
    oldTeam = teaming.teams.get(oldTid)
    
    if oldTeam and newTeam != oldTeam and oldTeam['players'][pid]:
        del oldTeam['players'][pid]
    
    if newTeam and newTeam != oldTeam:
        newTeam['players'][player['id']] = player
        
    if not newTeam:
        data['tid'] = None
    
    for key, val in data.items():
        if key in player: #only change exiting fields
            player[key] = val
    
    return player

@app.get('/backend/players/<pid>/remove') #testing only
@app.delete('/backend/players/<pid>') 
def teamPlayerDelete(pid):
    """Delete player"""
    try:
        pid = int(pid)
    except ValueError:
        bottle.abort(400, "Invalid player id %s" % pid)
        
    player = teaming.players.get(pid, None)
    if not player:
        bottle.abort(404, "Player '%s' not found." % (pid,))
    
    tid = player.get('tid')
    team = teaming.teams.get(tid) if tid else none    
    
    if team['players'][player['id']]:
        del team['players'][player['id']]
    
    del teaming.players[player['id']]
    
    return {}
