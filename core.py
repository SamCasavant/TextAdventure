from parser import parse
from world import worldInit
from actors import actorList

player = worldInit()
print("I wake up and look around.")
player.look()
#Main Loop:
while(1):
    player_move = parse(player, input())
    if player_move:
        player.act(player_move)
        for actor in actorList:
            actor.act()
            actor.update()
