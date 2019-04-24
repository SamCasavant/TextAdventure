
class Space():
    def __init__(self, name, description, visibleLocations = [], audibleLocations = []):
        self.name = name
        self.description= description
        self.visibleLocations = [self]
        self.audibleLocations = [self]
        self.connections = []
        self.actors = []
        self.things = []

    def addActors(self, actors):
        for actor in actors:
            self.actors.append(actor)
            actor.location = self

    def removeActor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)
        
    def addThings(self, things):
        for thing in things:
            self.things.append(thing)
            thing.location = self

    def removeThing(self, thing):
        if thing in self.things:
            self.things.remove(thing)
    
class Connection():
    def __init__(self, loc_a, loc_b, dir_a, dir_b, blocked = False, blockreason = "", visible=0, audible=1):
        self.loc_a = loc_a
        self.loc_b = loc_b
        self.dir_a = dir_a
        self.dir_b = dir_b
        self.blocked = blocked
        loc_a.connections.append(self)
        loc_b.connections.append(self)
        self.visible = visible
        self.audible = audible
    def getDest(self, location):
        if location == self.loc_a:
            return self.loc_b
        elif location == self.loc_b:
            return self.loc_a
    def getDir(self, actor):
        if actor.location == self.loc_a:
            return self.dir_a
        elif actor.location == self.loc_b:
            return self.dir_b
    
    def unblock(self):
        self.blocked = False
    def block(self, blockreason = ""):
        self.blocked = True
        self.blockreason = blockreason

def findPath(starts, ends, visitedNodes=[]): #takes a list of starting points and ending points, returns a path
    startMoves = [] #Locations that can be accessed from starts
    endMoves = [] #Locations that can be accessed from ends
    #First: See if any starts connect to any ends; build list of startMoves:
    for loc_a in starts:
        for move in [connection.getDest(loc_a) for connection in loc_a.connections]:
            if move in ends:
                return [loc_a, move]
            else:
                if move not in visitedNodes:
                    startMoves.append(move)
                    visitedNodes.append(move)
    #Second: See if there is a midpoint that connects any starts to any ends; build list of endMoves:
    for loc_b in ends:
        for move in [connection.getDest(loc_b) for connection in loc_b.connections]:
            if move in startMoves:
                for loc_a in starts:
                    if move in [connection.getDest(loc_a) for connection in loc_a.connections]:
                        return [loc_a, move, loc_b]
            else:
                if move not in visitedNodes:
                    endMoves.append(move)
                    visitedNodes.append(move)
    #Third: (Recursive) Try to find path between startMoves and endMoves; build path:
    interPath = findPath(startMoves, endMoves, visitedNodes)
    for loc_a in starts:
        if interPath[0] in [connection.getDest(loc_a) for connection in loc_a.connections]:
            path = [loc_a]
            break
    for loc_b in ends:
        if interPath[-1] in [connection.getDest(loc_b) for connection in loc_b.connections]:
            path.append(loc_b)
            break
    index = 1
    for element in interPath:
        path.insert(index, element)
        index+=1
    return path


# class Building():
#     def __init__(self, floors, rooms_per_floor, vertical = ['The stairwell'], special_rooms = []):
#         self.lobbies = []
#         for f in range(0,self.floors):
#             lobby = Space("Floor "+str(f)+" lobby", "A lobby connecting several rooms to the stairs.")
#             vertical = Space("Floor "+str(f)+" stairwell.")
#             lobby.addExits(())
#             for r in range(0, rooms_per_floor):
#                 room = Space("Room "+str(r)+"on floor "+str(f), "A typical room.")