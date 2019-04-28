import space
import things
import random
import output
from chrono import TIME


player = None
actorList = []


class Actor:  # This is a real class actor.
    def name(self, formal=False):
        return self.getName(formal)

    def update(self):
        self.updateStatus()

    def act(self):
        plan = self.createPlan()
        result = self.executePlan(plan)
        return result

    def move(self, destination):
        self.location.actors.remove(self)
        self.location = destination
        self.location.actors.append(self)
        return [1, [f"{self.name()} moves to {destination.name}", self, "move"]]

    def take(self, thing):
        if self.canTakeThing(thing):
            self.takeThing(thing)
            self.inventory.append(thing)
            return [1, [f"{self.name()} picks up {thing.name}.", self, "take"]]
        else:
            return [
                0,
                [
                    f"{self.name()} tries to pick up {thing.name} but cannot.",
                    self,
                    "take",
                ],
            ]

    def eat(self, thing):
        if self.canEatThing(thing):
            self.eatThing(thing)
            return [1, [f"{self.name()} eats {thing.name}.", self, "eat"]]
        else:
            return [
                0,
                [f"{self.name()} tries to eat {thing.name}, but cannot.", self, "eat"],
            ]

    def drink(self, thing):
        if self.canDrinkThing(thing):
            self.drinkThing(thing)
            return [1, [f"{self.name()} drinks {thing.name}.", self, "drink"]]
        else:
            return [
                0,
                [
                    f"{self.name()} tries to drink {thing.name}, but cannot.",
                    self,
                    "drink",
                ],
            ]


class AnimalPhysicalMixin:
    def getName(self, formal):
        if formal:
            return self.properName
        else:
            return self.commonName

    def updateStatus(self):
        self.states["eat"] += 0.1 * self.hunger_rate
        self.states["drink"] += 0.1 * self.thirst_rate
        if self.states["eat"] > 10:
            self.addWant("eat")
        if self.states["drink"] > 10:
            self.addWant("drink")

    def addWant(self, want):
        if want not in self.wants:
            self.wants.append(want)

    def executePlan(self, plan):
        if len(plan) > 0:
            action = plan[0]
            if action[0] == "move":
                result = self.move(action[1].getDest(self.location))
            elif action[0] == "take":
                result = self.take(action[1])
            elif action[0] == "eat":
                result = self.eat(action[1])
            elif action[0] == "wait":
                result = [1, [f"{self.properName} is waiting.", self, "wait"]]
            else:
                result = [
                    0,
                    [
                        f"{self.properName} attempts to {action[0]} but doesn't know how.",
                        self,
                        None,
                    ],
                ]
            if action[:-1] in [item[1] for item in self.itinerary]:
                index = [item[1] for item in self.itinerary].index(action[:-1])
                del self.itinerary[index]
        return result

    def talk(self):
        print(f"{self.properName} {random.choice(self.sounds)}s loudly.")

    def canTakeThing(self, thing):
        if "take" in thing.tags:
            if len(self.inventory) < self.max_inv:
                return True

    def takeThing(self, thing):
        self.inventory.append(thing)
        thing.take()

    def canEatThing(self, thing):
        if thing in self.inventory:
            if "eat" in thing.tags:
                return True
        elif thing in self.location.things:
            if "take_req" not in thing.tags:
                return True
            else:
                return False
        else:
            return False

    def eatThing(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states["eat"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["eat"] -= thing.eat_val

    def canDrinkThing(self, thing):
        if thing in self.inventory:
            if "drink" in thing.tags:
                return True
        elif thing in self.location.things:
            if "take_req" not in thing.tags:
                return True
            else:
                return False
        else:
            return False

    def drinkThing(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states["drink"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["drink"] -= thing.eat_val


class AnimalAIMixin:
    def createPlan(self):
        plan = []
        # Choose actions that result from status
        for want in self.wants:
            if self.strategies[want] == "search":
                find = self.search(want)
                if find:
                    plan.append(find)
                else:
                    if "move" not in [plan[0] for plan in plan]:
                        move = self.findMove()
                        if move:
                            plan.append(["move", move, self.states[want]])
        if len(plan) == 0:
            plan.append(["wait", 0])
        plan.sort(key=lambda x: x[-1], reverse=True)
        return plan

    def findMove(self):
        moves = []
        for connection in self.location.connections:
            if connection.blocked == False:
                moves.append(connection)
        if moves:
            return random.choice(moves)
        else:
            return False

    def getStrategy(self, want):
        try:
            strategy = self.strategies[want]
            return strategy
        except ValueError:
            return "search"

    def search(self, want):
        for thing in self.inventory:
            if want in thing.tags:
                return [want, thing, self.states[want]]
        else:
            for thing in self.location.things:
                if want in thing.tags:
                    if "take_req" in thing.tags:
                        if "take" in thing.tags:
                            return ["take", thing, self.states[want]]
                    else:
                        return [want, thing, self.states[want]]
            else:
                return None


class HumanPhysicalMixin:
    def getName(self, formal):
        if formal:
            return self.properName
        else:
            return self.commonName

    def executePlan(self, plan):
        if len(plan) > 0:
            action = plan[0]
            if action[0] == "move":
                result = self.move(action[1].getDest(self.location))
            elif action[0] == "take":
                result = self.take(action[1])
            elif action[0] == "eat":
                result = self.eat(action[1])
            elif action[0] == "wait":
                result = [1, [f"{self.properName} is waiting.", self, "wait"]]
            else:
                result = [
                    0,
                    [
                        f"{self.properName} attempts to {action[0]} but doesn't know how.",
                        self,
                        None,
                    ],
                ]
            if action[:-1] in [item[1] for item in self.itinerary]:
                index = [item[1] for item in self.itinerary].index(action[:-1])
                del self.itinerary[index]
        return result

    def canTakeThing(self, thing):
        if "take" in thing.tags:
            if len(self.inventory) < self.max_inv:
                return True
            else:
                return False
        else:
            return False

    def takeThing(self, thing):
        self.inventory.append(thing)
        self.location.removeThing(thing)

    def canEatThing(self, thing):
        if thing in self.inventory:
            if "eat" in thing.tags:
                return True
        elif thing in self.location.things:
            if "take_req" not in thing.tags:
                return True
            else:
                return False
        else:
            return False

    def eatThing(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states["eat"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["eat"] -= thing.eat_val

    def canDrinkThing(self, thing):
        if thing in self.inventory:
            if "drink" in thing.tags:
                return True
        elif thing in self.location.things:
            if "take_req" not in thing.tags:
                return True
            else:
                return False
        else:
            return False

    def drinkThing(self, thing):
        if thing in self.inventory:
            self.inventory.remove(thing)
            self.states["drink"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["drink"] -= thing.eat_val


class HumanAIMixin:
    def createPlan(self):
        plan = []
        # Choose actions that result from status
        for want in self.wants:
            if self.strategies[want] == "search":
                find = self.search(want)
                if find:
                    plan.append(find)
                else:
                    if "move" not in [plan[0] for plan in plan]:
                        move = self.findMove()
                        if move:
                            plan.append(["move", move, self.states[want]])
        # Choose actions that result from long term plan
        if self.itinerary:
            if (
                self.itinerary[0][0] - 1200 < TIME.time
            ):  # If action is to be done in less than 20 minutes. TODO: Make dynamic
                plan.append(
                    [
                        self.itinerary[0][1][0],
                        self.itinerary[0][1][1],
                        1000 / (self.itinerary[0][0] - TIME.time + 1),
                    ]
                )
        if len(plan) == 0:
            plan.append(["wait", 0])
        plan.sort(key=lambda x: x[-1], reverse=True)
        return plan

    def findMove(self):
        moves = []
        for connection in self.location.connections:
            if connection.blocked == False:
                moves.append(connection)
        if moves:
            return random.choice(moves)
        else:
            return False

    def addItinerary(self, itinerary):
        for item in itinerary:
            self.itinerary.append(item)
        self.itinerary.sort()

    def getStrategy(self, want):
        try:
            strategy = self.strategies[want]
            return strategy
        except ValueError:
            return "search"

    def search(self, want):
        for thing in self.inventory:
            if want in thing.tags:
                return [want, thing, self.states[want]]
        else:
            for thing in self.location.things:
                if want in thing.tags:
                    if "take_req" in thing.tags:
                        if "take" in thing.tags:
                            return ["take", thing, self.states[want]]
                    else:
                        return [want, thing, self.states[want]]
            else:
                return None


class Human(Actor, HumanPhysicalMixin, HumanAIMixin, AnimalPhysicalMixin):
    def __init__(
        self,
        properName,
        commonName="person",
        description="A regular human being.",
        location=None,
        inventory=None,
        max_inv=5,
        hunger_rate=1,
        hunger=3,
        itinerary=None,
        plan=None,
        tags=None,
        thirst=3,
        thirst_rate=1,
        wants=None,
        strategies=None,
    ):
        if inventory is None:
            inventory = []
        if itinerary is None:
            itinerary = []
        if plan is None:
            plan = []
        if tags is None:
            tags = ["human"]
        if wants is None:
            wants = []
        if strategies is None:
            strategies = {"eat": "search", "drink": "search", "money": "search"}
        self.properName = properName
        self.commonName = commonName
        self.description = description
        self.commonName = commonName
        self.description = description
        self.location = location
        self.inventory = inventory
        self.max_inv = max_inv
        self.states = {"eat": hunger, "drink": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        self.wants = wants
        self.strategies = strategies
        if itinerary:
            self.itinerary = itinerary.sort()
        else:
            self.itinerary = []
        actorList.append(self)


class User(Actor, HumanPhysicalMixin, AnimalPhysicalMixin):
    def __init__(
        self,
        properName,
        commonName="me",
        description="This is the person that I am.",
        location=0,
        inventory=[],
        max_inv=10,
        hunger_rate=1,
        hunger=3,
        thirst_rate=1,
        thirst=3,
        tags=["human", "user"],
    ):
        self.properName = properName
        self.commonName = commonName
        self.description = description
        self.location = location
        self.inventory = inventory
        self.max_inv = max_inv
        self.states = {"eat": hunger, "drink": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        actorList.append(self)

    def look(self):
        text = ""
        text += f"I am standing in {self.location.name}. {self.location.description}\n"
        if len(self.location.actors) > 2:
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
        if action[0] == "move":
            self.move(action[1].getDest(self.location))
            return [1, self.location, [f"I move to {self.location.name}", self, "move"]]
        elif action[0] == "take":
            self.take(action[1])
            return [1, self.location, [f"I pick up {action[1].name}", self, "take"]]
        elif action[0] == "look":
            self.look()
            return [0]
        elif action[0] == "look at":
            action[1].lookAt()
            return [0]
        elif action[0] == "open":
            action[1].open(self)
            return [1, self.location, [f"I open {action[1].name}", self, "open"]]
        elif action[0] == "close":
            action[1].close()
            return [1, self.location, [f"I close {action[1].name}", self, "close"]]
        elif action[0] == "inventory":
            self.chk_inventory()
            return [0]
        elif action[0] == "wait":
            return [1, self.location, ["I wait.", self, "wait"]]


class HouseCat(Actor, AnimalPhysicalMixin, AnimalAIMixin):
    def __init__(
        self,
        commonName="Cat",
        properName=None,
        description=None,
        location=0,
        inventory=None,
        max_inv=1,
        plan=None,
        hunger_rate=1,
        hunger=3,
        thirst_rate=1,
        thirst=3,
        tags=None,
        sounds=None,
        wants=None,
    ):
        if inventory is None:
            inventory = []
        if itinerary is None:
            itinerary = []
        if plan is None:
            plan = []
        if tags is None:
            tags = ["human"]
        if sounds is None:
            sounds = ["meow", "purr"]
        if wants is None:
            wants = []
        if not properName:
            self.properName = commonName
        else:
            self.properName = properName
        self.commonName = commonName
        self.description = description
        self.location = location
        self.inventory = inventory
        self.max_inv = max_inv
        self.plan = plan
        self.states = {"eat": hunger, "drink": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        self.sounds = sounds
        self.wants = wants
        actorList.append(self)
