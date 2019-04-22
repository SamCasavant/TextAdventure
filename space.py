
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
    def getDest(self, actor):
        if actor.location == self.loc_a:
            return self.loc_b
        elif actor.location == self.loc_b:
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


# class Building():
#     def __init__(self, floors, rooms_per_floor, vertical = ['The stairwell'], special_rooms = []):
#         self.lobbies = []
#         for f in range(0,self.floors):
#             lobby = Space("Floor "+str(f)+" lobby", "A lobby connecting several rooms to the stairs.")
#             vertical = Space("Floor "+str(f)+" stairwell.")
#             lobby.addExits(())
#             for r in range(0, rooms_per_floor):
#                 room = Space("Room "+str(r)+"on floor "+str(f), "A typical room.")
                
