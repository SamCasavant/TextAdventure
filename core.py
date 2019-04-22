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
        result = player.act(player_move)#returns outcome of format [bool Success, location, output]
        output.report(result, verbose=True)
        if result[0]:
            for actor in actorList:
                if 'user' not in actor.tags:
                    result = actor.act()
                    output.report(result, verbose=True)
                    actor.update()
            time.tick()
