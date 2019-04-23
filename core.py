from parser import parse
from world import worldInit
from actors import actorList
import chrono
import output

time = chrono.Chrono(18000, step=300)#Start time at 5AM, 5 minutes at a time

player = worldInit()
print("I wake up and look around.")
player.look()
#Main Loop:
while(1):
    player_move = parse(player, input())#returns move of format ['verb', 'object']
    if player_move:
        result = player.act(player_move)#returns outcome of format [bool Success, location, event ([output, actor, verb])]
        output.report(player, result, verbose=True)
        if result[0]: #if the action took time
            for actor in actorList:
                if 'user' not in actor.tags:
                    result = actor.act()
                    output.report(player, result[2], result[1], verbose=True) 
                    actor.update()
            time.tick()
