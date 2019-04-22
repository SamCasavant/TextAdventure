import space
import things
import random
import output

player = None
actorList = []
stateToDesire = {'hungry':'eat', 'thirsty':'drink'}

class Actor(things.Thing):
    def __init__(self, properName, commonName="", description = False, location=0, inventory = [], max_inv = 10, plan = [],
     hunger_rate = 1, hunger = 3, thirst_rate = 1, thirst = 3, tags = []):
        self.properName = properName
        self.commonName = commonName
        if description:
            self.description = description
        else:
            self.description = commonName
        self.inventory = inventory
        self.max_inv = max_inv
        self.plan = plan
        self.states = {'hungry':hunger, 'thirsty':thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.location = location
        self.tags = tags
        if location:
            location.addActors([self])
        actorList.append(self)

    def update(self):
        self.states['hungry'] += .1 * self.hunger_rate
        self.states['thirsty'] += .1 * self.thirst_rate
        if self.states['hungry']>10:
            if 'hungry' not in self.tags:
                self.tags.append('hungry')
        if self.states['thirsty']>10:
            if 'thirsty' not in self.tags:
                self.tags.append('thirsty')

    def act(self):
        if len(self.plan)>0:
            action = self.plan[0]
            if action[0] == 'move':
                self.move(action[1])
            elif action[0] == 'take':
                self.take(action[1])
                output.visOutput(player, [self.location], f"{self.properName} picks up {action[1].name}.")
            elif action[0] == 'eat':
                self.eat(action[1])
                output.visOutput(player, [self.location], f"{self.properName} eats {action[1].name}.")
            elif action[0] == 'wait':
                output.visOutput(player, [self.location], f"{self.properName} is waiting.")
                pass
            else:
                output.visOutput(player, [self.location], f"{self.properName} attempts to {action[0]} but doesn't know how.")
            self.plan.pop(0)
        else:
            self.createPlan()
            self.act()
        
    def createPlan(self):
        for adj in self.states.keys():
            if adj in self.tags:
                desire = stateToDesire[adj]
                for thing in self.inventory:
                    if desire in thing.tags:
                        self.plan.append([desire, thing, self.states[adj]])
                    break
                else:
                    for thing in self.location.things:
                        if desire in thing.tags:
                            if 'take_req' in thing.tags:
                                if 'take' in thing.tags:
                                    self.plan.append(['take', thing, self.states[adj]])
                                    break
                            else:
                                self.plan.append([desire, thing, self.states[adj]])
                    else:
                        if 'move' not in [plan[0] for plan in self.plan]:
                            move = self.findMove()
                            if move:
                                self.plan.append(['move', move, self.states[adj]])
        if len(self.plan)==0:
            self.plan.append(['wait', 0])  
        self.plan.sort(key = lambda x: x[-1], reverse = True) 

    def move(self, connection):
        if connection.blocked:
            output.visOutput(player, [self.location], f"{self.properName} tries to go to {connection.getDest(self).name}, but {connection.blockreason}")
        else:
            target = connection.getDest(self)
            eventLocations = [self.location, target]
            self.location.actors.remove(self)
            self.location = target
            self.location.actors.append(self)
            output.visOutput(player, eventLocations, f"{self.properName} goes to {self.location.name}.")

    def take(self, thing):
        if len(self.inventory)<self.max_inv: 
            attempt = thing.take()
            if attempt:
                self.inventory.append(thing)
    def eat(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states['hungry'] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states['hungry'] -= thing.eat_val
    def drink(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states['thirst'] -= thing.drink_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states['thirst'] -= thing.drink_val
    def findMove(self):
        moves = []
        for connection in self.location.connections:
            if connection.blocked == False:
                moves.append(connection)
        if moves:
            return random.choice(moves)
        else:
            return False




#def search

