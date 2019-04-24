from actors import Actor, player, actorList
import output
import random
from chrono import TIME

class Human(Actor):
    def __init__(self, properName, commonName='person', description = "A regular human being.", location = 0, inventory = [], max_inv = 5, hunger_rate = 1, hunger = 3, itinerary = [], plan = [], tags=['human']):
        super(Human, self).__init__(properName, commonName = commonName, description = description, location =location,
         inventory = inventory, max_inv = max_inv, hunger_rate = hunger_rate, hunger =hunger, tags=tags)
        if itinerary:
            self.itinerary = itinerary.sort()
        else:
            self.itinerary = []

    def createPlan(self):
        super(Human, self).createPlan()
        if self.itinerary:
            print(self.properName)
            if self.itinerary[0][0]-1200 < TIME.time: #If action is to be done in less than 20 minutes. TODO: Make dynamic
                if self.itinerary[0][1] in [item[0] for item in self.plan]:
                    index = [item[0] for item in self.plan].index(self.itinerary[0][1])
                    self.plan[index] = [self.itinerary[0][1], 1000/(self.itinerary[0][0]-TIME.time+1)]
                else:
                    self.plan.append([self.itinerary[0][1][0], self.itinerary[0][1][1], 1000/(self.itinerary[0][0]-TIME.time+1)])
            self.plan.sort(key = lambda x: x[-1], reverse = True) 
        
    def addItinerary(self, itinerary):
        for item in itinerary:
            self.itinerary.append(item)
        itinerary.sort()



class User(Human):
    def __init__(self, properName, commonName = "me", description = "This is the person that I am.", location = 0, inventory = [], max_inv = 10, hunger_rate = 1, hunger = 3,tags = ['human', 'user']):
        super(User, self).__init__(properName, commonName, description, location, inventory, max_inv, hunger_rate, hunger, tags=tags)
        
    def look(self):
        text = ""
        text+=f"I am standing in {self.location.name}. {self.location.description}\n"
        if len(self.location.actors)>2:
            verbIs = "are"
        else:
            verbIs = "is"
        text += f"{output.listToNatural([actor.properName for actor in self.location.actors if 'user' not in actor.tags])} {verbIs} here.\n"
        text += f"I can see {output.listToNatural([thing.name for thing in self.location.things])}.\n"
        print(text)
    def chk_inventory(self):
        if self.inventory:
            print("I have:")
            for thing in self.inventory:
                print(thing.name)
        else:
            print("I don't have anything at the moment.")
    def act(self, action):
        if action[0] == 'move':
            self.move(action[1])
            return([1, self.location, [f"I move to {self.location.name}", self, 'move']])
        elif action[0] == 'take':
            self.take(action[1])
            return([1, self.location, [f"I pick up {action[1].name}", self, 'take']])
        elif action[0] == 'look':
            self.look()
            return[0]
        elif action[0] == 'look at':
            action[1].lookAt()
            return [0]
        elif action[0] == 'open':
            action[1].open(self)
            return([1, self.location, [f"I open {action[1].name}", self, 'open']])
        elif action[0] == 'close':
            action[1].close()
            return([1, self.location, [f"I close {action[1].name}", self, 'close']])
        elif action[0] == 'inventory':
            self.chk_inventory()
            return [0]
        elif action[0] == 'wait':
            return([1, self.location, ["I wait.", self, 'wait']])



class Animal(Actor):
    def __init__(self, commonName, properName = "", description = False, location=0, inventory = [], max_inv = 1, plan = [], hunger_rate = 1,
                 hunger = 3, thirst_rate = 1, thirst = 3, tags = [], sounds = []):
        if not properName:
            properName = commonName
        super(Animal, self).__init__(properName, commonName, description, location, inventory, max_inv, 
        plan, hunger_rate, hunger, thirst_rate, thirst, tags)
        self.sounds = sounds
    def talk(self):
        print(f"{self.properName} {random.choice(self.sounds)}s loudly.")

class Housecat(Animal):
    def __init__(self, properName="", commonName="cat", description = False, inventory = [], max_inv=1, location = 0, plan = [],
                 tags = [], hunger_rate = 1, hunger = 3, thirst_rate = 1, thirst = 3, sounds = ['meow', 'purr']):
        super(Housecat, self).__init__(commonName, properName, description, location, inventory, max_inv, 
        plan, hunger_rate, hunger, thirst_rate, thirst, tags, sounds)