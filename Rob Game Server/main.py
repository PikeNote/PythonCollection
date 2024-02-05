import asyncio
import os
import json;
import aiohttp.web
from random import randint



# Store active clients in this dictionary when they are connected
active_games = {
  
}


HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')


    # Basic JSON structure structure
    """
    {
      "type":(string), // (close/gameData/createLobby/joinLobby)/establishedConnection
      "user":(string), //uuid of the user? will depend for now
      "payload":data // depends on the data being sent
    }
    """

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
          try:
            jsonData = json.loads(msg.data);
          
            match jsonData["type"]:
              # Close connection
              case "close":
                await ws.close()
              # Take any game data sent and then rebroadcast it to the other user
              case "gameData":
                # Include match_uuid in the request to the server 
                match_uuid = ws["uuid"];
                

                # Transfer the data from the intially sent payload to the
                # data sent to the otehr clients
                jsonRes = {"type":jsonData["payload"]["type"],
                  "payload":
                    jsonData["payload"]["payload"]
                }
                # Send to the other player
                # The "user" field in the JSON sent is if the user is player 1 
                # or 2
                playerToSendTo = 1 if ws["player"] == 0 else 0;

                await active_games[match_uuid]["players"][playerToSendTo].send_json({"type":"gameData","payload":jsonRes})

                  
                pass
              case "createLobby":
                # Create a new unique UUID for the server
                # Add the game to the active games dictionary
                match_uuid = str(f"{randint(10000000, 99999999)}")
                active_games[match_uuid] = {
                  "players": [ws],
                  "playerNames": [jsonData["payload"]["name"]],
                  "scores":[0,0],
                  "received": [False,False],
                  "started": False
                }
                ws["uuid"] = match_uuid;
                ws["player"] = 0;
                await ws.send_json({"type":"lobbyCreated","payload":{"game_id":match_uuid}});
                
              case "joinLobby":
                # Include match_uuid/match_id ini the request
                match_uuid = jsonData["payload"]["match_uuid"];

                # Check if match exists
                if(match_uuid in active_games):
                  # Send every client in the lobby information
                  # that a new player has joined

                  for w in active_games[match_uuid]["players"]:
                    await w.send_json({"type":"lobbyJoined","payload":{"name":jsonData["payload"]["name"]}});
                  
                 # await active_games[match_uuid]["players"][0].send_json({"type":"lobbyJoined","payload":{"name":jsonData["payload"]["name"]}});
                    
                  active_games[match_uuid]["players"].append(ws);


                  active_games[match_uuid]["playerNames"].append(jsonData["payload"]["name"])
                  # Send the lobby sucessfully joined back to the sending7416
                  # client
                  ws["uuid"] = match_uuid
                  ws["player"] = len(active_games[match_uuid]["players"])-1;
                  print("Assigned id:" + str(ws["player"]))
                  await ws.send_json({
                    "type":"lobbyStatus",
                    "payload":{
                      "status":1,
                      "playerNames":active_games[match_uuid]["playerNames"],
                      "match_uuid":match_uuid
                    }
                  });
                else:
                  await ws.send_json({
                    "type":"lobbyStatus",
                    "payload":{
                      "status":0
                    }
                  });
                pass
              case "lobbyStarted":
                if(match_uuid in active_games):
                  await active_games[match_uuid]["players"][1].send_json({"type":"lobbyStarted"});
              case "establishedConnection":
                
                pass
              case "readyGame":
                if(ws["uuid"] in active_games):
                  ws["uuid"]["started"] = True;
                  await active_games[ws["uuid"]]["players"][0].send_json({"type":"startSpawn"});
                pass;
              case "gameEnded":
                match_uuid = jsonData["payload"]["match_uuid"];
                player = jsonData["user"]
                matchScores = active_games[match_uuid]["scores"];
                # Check if match exists
                if(match_uuid in active_games):
                  matchScores[player] = jsonData["payload"]["points"];
                  active_games[match_uuid]["received"][player] = True;

                  if(active_games[match_uuid]["received"][0] and active_games[match_uuid]["received"][1]):
                    playerWon = 0;
                    if(matchScores[0] < matchScores[1]):
                      playerWon = 1;
                    elif(matchScores[0] == matchScores[1]):
                      playerWon = -1;

                    jsonRes = {
                      "scores":matchScores,
                      "winner": playerWon
                    }
                    wsConn = active_games[match_uuid]["players"];
                    active_games.pop(match_uuid, None);
                    for w in wsConn:
                      await w.send_json({"type":"gameEnded","payload":jsonRes})
                      w.close();

                    
          
            
          except:
            print("Invalid sent information") 
              
    if(ws["uuid"] in active_games):
      currentGame = active_games[ws["uuid"]]
      if(currentGame["started"]):
        playerToSendTo = 1 if ws["player"] == 0 else 0;
        jsonRes = {
          "scores": currentGame["scores"],
          "winner": playerToSendTo
        }
        await active_games[ws["uuid"]]["players"][playerToSendTo].send_json({"type":"gameEnded","payload":jsonRes})
        otherWs = currentGame["players"][playerToSendTo];
        active_games.pop(ws["uuid"], None);
        await otherWs.close();
      else:
        if len(currentGame["players"]) > 1:
          playerToSendTo = 1 if ws["player"] == 0 else 0;
          otherWs = currentGame["players"][playerToSendTo];
          active_games.pop(ws["uuid"], None);
          await otherWs.close();
    print('Websocket connection closed')
    return ws

  #Basic user authentication to be implemented later
"""
async def login(request):
  body = await request.json()
  if(body.username && body.password):
    if db.collection.count_documents({ 'username': body.username }, limit = 1):
        ph = PasswordHasher()
        user = db.user_data.user_login.find( { "username": body.username)
        user.next(function(err, doc) {
          if (doc) {
              try:
                ph.verify(doc.password, body.password)
                if ph.check_needs_rehash(doc.password):
                  doc.password = ph.hash(password)
              except:
                pass
          }
        });
    else:
        pass
"""    
# Basic base URL response
async def status(request):
  return aiohttp.web.Response(status=200, body="Online!");

def main():
  
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/ws', websocket_handler)
    app.router.add_route('GET', '/', status)
    
    asyncio.run(aiohttp.web.run_app(app, host=HOST, port=PORT))


if __name__ == '__main__':
    main()
    print("Server started")