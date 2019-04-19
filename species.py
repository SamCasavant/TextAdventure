from actors import Actor, player, actorList
import output
import random

class Human(Actor):
    def __init__(self, properName, commonName='person', description = "A regular human being.", location = 0, inventory = [], max_inv = 5, hunger_rate = 1, hunger = 3, itinerary = [], plan = [], tags=['human']):
        super(Human, self).__init__(properName, commonName, description, location, inventory, max_inv, hunger_rate, hunger, tags=tags)
        self.itinerary = itinerary

    def act_plan(self):
        super.plan()
        if len(self.plan)<1:
            self.plan.append(self.itinerary[0])


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