import space
import things
import random
import output
from chrono import TIME


player = None
actorList = []


class Actor:
    # def __init__(
    #     self,
    #     properName,
    #     commonName="",
    #     description=False,
    #     location=0,
    #     inventory=[],
    #     max_inv=10,
    #     plan=[],
    #     hunger_rate=1,
    #     hunger=3,
    #     thirst_rate=1,
    #     thirst=3,
    #     tags=[],
    # ):
    #     self.properName = properName
    #     self.commonName = commonName
    #     if description:
    #         self.description = description
    #     else:
    #         self.description = commonName
    #     self.inventory = inventory
    #     self.max_inv = max_inv
    #     self.plan = plan
    #
    #     self.hunger_rate = hunger_rate
    #     self.thirst_rate = thirst_rate
    #     self.location = location
    #     self.tags = tags
    #     if location:
    #         location.addActors([self])
    #
    def name(self, formal=False):
        return self.getName(formal)

    def update(self):
        self.updateStates()

    def act(self):
        plan = self.createPlan()
        result = self.executePlan(plan)
        return result

    def move(self, destination):
        self.location.actors.remove(self)
        self.location = destination
        self.location.actors.append(self)

    def take(self, thing):
        if self.canTakeThing(thing):
            self.takeThing(thing)
            self.inventory.append(thing)

    def eat(self, thing):
        if self.canEatThing(thing):
            self.eatThing(thing)

    def drink(self, thing):
        if self.canDrinkThing(thing):
            self.drinkThing(thing)


class AnimalPhysicalMixin:
    def getName(self, formal):
        if formal:
            return self.properName
        else:
            return self.commonName

    def updateStates(self):
        self.states["hungry"] += 0.1 * self.hunger_rate
        self.states["thirsty"] += 0.1 * self.thirst_rate
        if self.states["hungry"] > 10:
            print(self.name())
            if "hungry" not in self.tags:
                self.tags.append("hungry")
        if self.states["thirsty"] > 10:
            if "thirsty" not in self.tags:
                self.tags.append("thirsty")

    def executePlan(self, plan):
        if len(plan) > 0:
            action = plan[0]
            if action[0] == "move":
                self.move(action[1].getDest(self.location))
                return [
                    1,
                    self.location,
                    [f"{self.properName} moves to {self.location.name}", self, "take"],
                ]
            elif action[0] == "take":
                self.take(action[1])
                return [
                    1,
                    self.location,
                    [f"{self.properName} picks up {action[1].name}", self, "take"],
                ]
            elif action[0] == "eat":
                self.eat(action[1])
                return [
                    1,
                    self.location,
                    [f"{self.properName} eats {action[1].name}.", self, "eat"],
                ]
            elif action[0] == "wait":
                return [
                    1,
                    self.location,
                    [f"{self.properName} is waiting.", self, "wait"],
                ]
            else:
                return [
                    0,
                    self.location,
                    [
                        f"{self.properName} attempts to {action[0]} but doesn't know how.",
                        self,
                        None,
                    ],
                ]

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
            self.states["hungry"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["hungry"] -= thing.eat_val

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
            self.states["thirsty"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["thirsty"] -= thing.eat_val


class AnimalAIMixin:
    def createPlan(self):
        plan = []
        stateToDesire = {"hungry": "eat", "thirsty": "drink"}
        for adj in self.states.keys():
            if adj in self.tags:
                desire = stateToDesire[adj]
                for thing in self.inventory:
                    if desire in thing.tags:
                        plan.append([desire, thing, self.states[adj]])
                    break
                else:
                    for thing in self.location.things:
                        if desire in thing.tags:
                            if "take_req" in thing.tags:
                                if "take" in thing.tags:
                                    plan.append(["take", thing, self.states[adj]])
                                    break
                            else:
                                plan.append([desire, thing, self.states[adj]])
                    else:
                        if "move" not in [plan[0] for plan in plan]:
                            move = self.findMove()
                            if move:
                                plan.append(["move", move, self.states[adj]])
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


class HumanPhysicalMixin:
    def getName(self, formal):
        if formal:
            return self.properName
        else:
            return self.commonName

    def executePlan(self, plan):
        if len(plan) > 0:
            action = plan[0]
            print(action)
            print(self.itinerary)
            if action[:-1] in [item[1] for item in self.itinerary]:
                print("Hey this should work")
                index = [item[1] for item in self.itinerary].index(action[:-1])
                del self.itinerary[index]

            if action[0] == "move":
                self.move(action[1].getDest(self.location))
                return [
                    1,
                    self.location,
                    [f"{self.properName} moves to {self.location.name}", self, "take"],
                ]
            elif action[0] == "take":
                self.take(action[1])
                return [
                    1,
                    self.location,
                    [f"{self.properName} picks up {action[1].name}", self, "take"],
                ]
            elif action[0] == "eat":
                self.eat(action[1])
                return [
                    1,
                    self.location,
                    [f"{self.properName} eats {action[1].name}.", self, "eat"],
                ]
            elif action[0] == "wait":
                return [
                    1,
                    self.location,
                    [f"{self.properName} is waiting.", self, "wait"],
                ]
            else:
                return [
                    0,
                    self.location,
                    [
                        f"{self.properName} attempts to {action[0]} but doesn't know how.",
                        self,
                        None,
                    ],
                ]

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
            self.states["hungry"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["hungry"] -= thing.eat_val

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
            self.states["thirsty"] -= thing.eat_val
        elif thing in self.location.things:
            self.location.removeThing(thing)
            self.states["thirsty"] -= thing.eat_val


class HumanAIMixin:
    def createPlan(self):
        plan = []
        stateToDesire = {"hungry": "eat", "thirsty": "drink"}
        for adj in self.states.keys():
            if adj in self.tags:
                desire = stateToDesire[adj]
                for thing in self.inventory:
                    if desire in thing.tags:
                        plan.append([desire, thing, self.states[adj]])
                    break
                else:
                    for thing in self.location.things:
                        if desire in thing.tags:
                            if "take_req" in thing.tags:
                                if "take" in thing.tags:
                                    plan.append(["take", thing, self.states[adj]])
                                    break
                            else:
                                plan.append([desire, thing, self.states[adj]])
                    else:
                        if "move" not in [plan[0] for plan in plan]:
                            move = self.findMove()
                            if move:
                                plan.append(["move", move, self.states[adj]])
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
    ):
        if inventory is None:
            inventory = []
        if itinerary is None:
            itinerary = []
        if plan is None:
            plan = []
        if tags is None:
            tags = ["human"]

        self.properName = properName
        self.commonName = commonName
        self.description = description
        self.commonName = commonName
        self.description = description
        self.location = location
        self.inventory = inventory
        self.max_inv = max_inv
        self.states = {"hungry": hunger, "thirsty": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
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
        self.states = {"hungry": hunger, "thirsty": thirst}
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
        self.states = {"hungry": hunger, "thirsty": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        self.sounds = sounds
        actorList.append(self)
