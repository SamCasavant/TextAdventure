from parser import parse
from world2 import worldInit
from actors import actorList
from chrono import TIME
import time
from multiprocessing import Process
import output


# Main Loop:
def actorLoop(rate):
    curTime = time.perf_counter()
    while 1:
        if time.perf_counter() - curTime >= 1:
            print(time.perf_counter() - curTime)
            curTime = time.perf_counter()
            for actor in actorList:
                if "user" not in actor.tags:
                    result = actor.act()
                    if result[0]:
                        output.report(player, result[1], verbose=True)
                    actor.update()
            TIME.tick()
            print(TIME.getTime("clock"))


def playerLoop():
    while 1:
        player_move = parse(
            player, input()
        )  # returns move of format ['verb', 'object']
        if player_move:
            result = player.act(
                player_move
            )  # returns outcome of format [bool Success, location, event ([output, actor, verb])]
            output.report(player, result, verbose=True)


### 'Wait for player input' version.
# while 1:
#     player_move = parse(player, input())  # returns move of format ['verb', 'object']
#     if player_move:
#         result = player.act(
#             player_move
#         )  # returns outcome of format [bool Success, location, event ([output, actor, verb])]
#         output.report(player, result, verbose=True)
#         if result[0]:  # if the action took time
#             for actor in actorList:
#                 if "user" not in actor.tags:
#                     result = actor.act()
#                     if result[0]:
#                         output.report(player, result[1], verbose=True)
#                     actor.update()
#             TIME.tick()
#             print(TIME.getTime("clock"))

if __name__ == "__main__":
    rate = 1  # ticks per second
    player = worldInit()
    print("I wake up and look around.")
    player.look()
    world = Process(target=actorLoop, args=(rate,))
    world.start()
    world.join()
    playerLoop()
