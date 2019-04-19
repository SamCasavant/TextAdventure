import space
import things
import random

player = None
actorList = []

class Actor(things.Thing):
    def __init__(self, name, description = False, location=0, inventory = [], max_inv = 10, plan = [],
     hunger_rate = 1, hunger = 3, thirst_rate = 1, thirst = 3, tags = []):
        self.name = name
        if description:
            self.description = description
        else:
            self.description = name
        self.inventory = inventory
        self.max_inv = max_inv
        self.plan = plan
        self.hunger = hunger
        self.hunger_rate = hunger_rate
        self.thirst = thirst
        self.thirst_rate = thirst_rate
        self.location = location
        self.tags = tags
        if location:
            location.addActors([self])
        actorList.append(self)

    def update(self):
        self.hunger += .1 * self.hunger_rate
        self.thirst += .1 * self.thirst_rate
        if self.hunger>10:
            if 'hungry' not in self.tags:
                self.tags.append('hungry')
        if self.thirst>10:
            if 'thirsty' not in self.tags:
                self.tags.append('thirsty')

    def act(self):
        if len(self.plan)>0:
            action = self.plan[0]
            if action[0] == 'move':
                oldLocation = self.location
                self.move(action[1])
                visOutput(self, f"{self.name} moves to {self.location.name}.", extraLocations=[oldLocation])
            elif action[0] == 'take':
                self.take(action[1])
                visOutput(self, f"{self.name} picks up {action[1].name}.")
            elif action[0] == 'eat':
                self.eat(action[1])
                visOutput(self, f"{self.name} eats {action[1].name}.")
            elif action[0] == 'wait':
                visOutput(self, f"{self.name} is waiting.")
                pass
            else:
                visOutput(self, f"{self.name} attempts to {action[0]} but doesn't know how.")
            self.plan.pop(0)
        else:
            self.createPlan()
            self.act()
        
    def createPlan(self):
        if 'hungry' in self.tags:
            for thing in self.inventory:
                if 'eat' in thing.tags:
                    self.plan.append(['eat', thing, self.hunger])
                    break
            else:
                for thing in self.location.things:
                    if 'eat' in thing.tags:
                        if 'take_req' in thing.tags:
                            if 'take' in thing.tags:
                                self.plan.append(['take', thing, self.hunger])
                                break
                        else:
                            self.plan.append(['eat', thing, self.hunger])
                else:
                    if 'move' not in [plan[0] for plan in self.plan]:
                        move = self.findMove()
                        if move:
                            self.plan.append(['move', move, self.hunger])
        if 'thirsty' in self.tags:
            for thing in self.inventory:
                if 'drink' in thing.tags:
                    self.plan.append(['drink', thing, self.thirst])
                    break
            else:
                for thing in self.location.things:
                    if 'drink' in thing.tags:
                        if 'take_req' in thing.tags:
                            if 'take' in thing.tags:
                                self.plan.append(['take', thing, self.thirst])
                                break
                        else:
                            self.plan.append(['drink', thing, self.thirst])
                else:
                    if 'move' not in [plan[0] for plan in self.plan]:
                        move = self.findMove()
                        self.plan.append(['move', move, self.thirst])
        if len(self.plan)==0:
            self.plan.append(['wait', 0])  
        self.plan.sort(key = lambda x: x[-1], reverse = True) 

    def move(self, destination):
        self.location.actors.remove(self)
        self.location = destination
        self.location.actors.append(self)

    def take(self, thing):
        if len(self.inventory)<self.max_inv: 
            attempt = thing.take()
            if attempt:
                self.inventory.append(thing)
    def eat(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.hunger -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.hunger -= thing.eat_val
    def drink(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.thirst -= thing.drink_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.thirst -= thing.drink_val
    def findMove(self):
        moves = []
        for connection in self.location.connections:
            if connection.blocked == False:
                moves.append(connection.getDest(self))
        if moves:
            return random.choice(moves)
        else:
            return False

class Human(Actor):
    def __init__(self, name, location = 0, itinerary = [], plan = [], hunger_rate = 1, hunger = 3):
        self.name = name
        self.itinerary = itinerary
        self.plan = plan
        self.hunger = hunger
        self.hunger_rate = hunger_rate
        self.hunger_rate = hunger_rate
        self.location = location
        if location:
            location.addActors([self])
        actorList.append(self)
    def act_plan(self):
        super.plan()
        if len(self.plan)<1:
            self.plan.append(self.itinerary[0])


class User(Human):
    def __init__(self, name, location = 0, inventory = [], max_inv = 10, hunger_rate = 1, hunger = 3,):
        self.name = name
        self.inventory = inventory
        self.max_inv = max_inv
        self.hunger = hunger
        self.hunger_rate = hunger_rate
        self.location = location
        if location:
            location.addActors([self])
    def look(self):
        print("I am standing in ", self.location.name, ".", sep = '')
        print(self.location.description)
        for actor in self.location.actors:
            if actor != self:
                print(actor.name, "is here.")
        for thing in self.location.things:
            print("There is ", thing.name, ".", sep = '')
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
            print("I go to ", self.location.name, ".", sep = '')
        elif action[0] == 'take':
            self.take(action[1])
            print("I pick up %s."% action[1].name)
        elif action[0] == 'look':
            self.look()
        elif action[0] == 'look at':
            action[1].lookAt()
        elif action[0] == 'open':
            action[1].open(self)
        elif action[0] == 'close':
            action[1].close()
        elif action[0] == 'inventory':
            self.chk_inventory()
        elif action[0] == 'wait':
            print("I wait.")


class Animal(Actor):
    def __init__(self, name, description = False, location=0, inventory = [], max_inv = 1, plan = [], hunger_rate = 1,
                 hunger = 3, thirst_rate = 1, thirst = 3, tags = [], sounds = []):
        super(Animal, self).__init__(name, description, location, inventory, max_inv, 
        plan, hunger_rate, hunger, thirst_rate, thirst, tags)
        self.sounds = sounds
    def talk(self):
        print(f"{self.name} {random.choice(self.sounds)}s loudly.")

class Housecat(Animal):
    def __init__(self, name="the cat", description = False, inventory = [], max_inv=1, location = 0, plan = [],
                 tags = [], hunger_rate = 1, hunger = 3, thirst_rate = 1, thirst = 3, sounds = ['meow', 'purr']):
        super(Housecat, self).__init__(name, description, location, inventory, max_inv, 
        plan, hunger_rate, hunger, thirst_rate, thirst, tags, sounds)


#def search
def visOutput(actor, output, extraLocations = []):
    if actor.location == player.location:
        print(output)
    else:
        for location in extraLocations:
            if location == player.location:
                print(output)
def audOutput(actor, output):
    if actor.location in player.listenLocations:
        print(output)