import space
import things
import random
import output
from chrono import TIME


player = None
actorList = []


class ActorMixin:  # This is a real class actor.
    """This class implements a set of basic functions that apply to all of the agents in the game."""

    def name(self, formal=False):
        return self.getName(formal)

    def update(self):
        self.updateStatus()

    def act(self):
        """Takes actions and returns a result of the form [successBool, [output, actor, verb]]"""
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
    """This class implements basic animal functions like hunger and thirst."""

    def getName(self, formal=False):
        if formal:
            return self.properName
        else:
            return self.commonName

    def updateStatus(self):
        self.states["eat"] += 0.1 * self.hunger_rate
        self.states["drink"] += 0.1 * self.thirst_rate

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
        for state in self.states.keys():
            if self.strategies[state] == "search":
                find = self.search(state)
                if find:
                    plan.append(find)
                else:
                    if "move" not in [plan[0] for plan in plan]:
                        move = self.findMove()
                        if move:
                            plan.append(["move", move, self.states[state]])
        plan.append(["wait", self.lazyThreshold])
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

    def getStrategy(self, state):
        try:
            strategy = self.strategies[state]
            return strategy
        except ValueError:
            return "search"

    def search(self, state):
        for thing in self.inventory:
            if state in thing.tags:
                return [state, thing, self.states[state]]
        else:
            for thing in self.location.things:
                if state in thing.tags:
                    if "take_req" in thing.tags:
                        if "take" in thing.tags:
                            return ["take", thing, self.states[state]]
                    else:
                        return [state, thing, self.states[state]]
            else:
                return None


class HumanPhysicalMixin:
    """This class implements physical properties that are applicable to humans."""

    def getName(
        self, formal=True
    ):  # Only different from animal getName by defaulting to formal.
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
    """This class implements a set of higher level planning and actions."""

    def createPlan(self):
        plan = []
        # Choose actions that result from status
        for state in self.states.keys():
            if self.strategies[state] == "search":
                find = self.search(state)
                if find:
                    plan.append(find)
                else:
                    if "move" not in [plan[0] for plan in plan]:
                        move = self.findMove()
                        if move:
                            plan.append(["move", move, self.states[state]])
            elif self.strategies[state] == "mug":
                action = self.mug(self.states[state])
                plan.append(action)
        # Choose actions that result from long term plan
        if self.itinerary:
            plan.append(
                [
                    self.itinerary[0][1][0],
                    self.itinerary[0][1][1],
                    1000 / (self.itinerary[0][0] - TIME.time + 1),
                ]
            )
        plan.append(["wait", self.lazyThreshold])
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

    def getStrategy(self, state):
        try:
            strategy = self.strategies[state]
            return strategy
        except ValueError:
            return "search"

    def search(self, state):
        for thing in self.inventory:
            if state in thing.tags:
                return [state, thing, self.states[state]]
        else:
            for thing in self.location.things:
                if state in thing.tags:
                    if "take_req" in thing.tags:
                        if "take" in thing.tags:
                            return ["take", thing, self.states[state]]
                    else:
                        return [state, thing, self.states[state]]
            else:
                return None

    def mug(self, priority):
        for condition in self.mugConditions:
            if isMet(condition):
                pass
            elif condition[1]<priority:
                pass
            else:

        self.mugConditions

    def isMet(self, condition):


class Human(ActorMixin, HumanPhysicalMixin, HumanAIMixin, AnimalPhysicalMixin):
    """Properties:
    States: A dictionary of potential causes of action and their degree of intensity, labeled according to the relevant verb (instead of 'hungry', 'eat') for internal consistency (where possible).
    Strategies: A dictionary that relates states to response strategies; only search is currently implemented.
    Itinerary: A list of planned actions and the time, in seconds since midnight, that it is supposed to occur by.
    Tags: A miscellanious collection of properties that impact what a character can do and what can be done to them.
    lazyThreshold: The priority given to 'wait' in the plan.
    Conditions: Prerequisites for strategies of the form ['property', 'value', 'priority'], eg. Grumph should have a weapon and would like an associate before attempting to mug, so conditions['mug']=[['have', 'weapon', 100], ['be', 'cooperating', 10]"""

    def __init__(
        self,
        properName,
        commonName="person",
        description="A regular human being.",
        inventory=None,
        max_inv=5,
        hunger_rate=1,
        hunger=3,
        itinerary=None,
        tags=None,
        thirst=3,
        thirst_rate=1,
        strategies=None,
        lazyThreshold=5,
    ):
        if inventory is None:
            inventory = []
        if itinerary is None:
            itinerary = []
        if tags is None:
            tags = ["human"]
        if strategies is None:
            strategies = {"eat": "search", "drink": "search", "money": "search"}
        self.plan = []
        self.states = {"eat": hunger, "drink": thirst}
        self.properName = properName
        self.commonName = commonName
        self.description = description
        self.inventory = inventory
        self.max_inv = max_inv
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        self.strategies = strategies
        self.lazyThreshold = lazyThreshold
        if itinerary:
            self.itinerary = itinerary.sort()
        else:
            self.itinerary = []
        actorList.append(self)


class User(ActorMixin, HumanPhysicalMixin, AnimalPhysicalMixin):
    def __init__(
        self,
        properName,
        commonName="me",
        description="This is the person that I am.",
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

    def chk_states(self):
        for state in self.states.keys():
            print(f"{state}: {self.states[state]}.")

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


class HouseCat(ActorMixin, AnimalPhysicalMixin, AnimalAIMixin):
    """Properties:
    States: A dictionary of potential causes of action and their degree of intensity, labeled according to the relevant verb (instead of 'hungry', 'eat') for internal consistency.
    Tags: A miscellanious collection of properties that impact what a character can do and what can be done to them.
    lazyThreshold: The priority given to 'wait' in the plan."""

    def __init__(
        self,
        commonName="Cat",
        properName=None,
        description=None,
        inventory=None,
        max_inv=1,
        hunger_rate=1,
        hunger=3,
        thirst_rate=1,
        thirst=3,
        tags=None,
        sounds=None,
        lazyThreshold=5,
    ):
        if inventory is None:
            inventory = []
        if itinerary is None:
            itinerary = []
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
        self.inventory = inventory
        self.max_inv = max_inv
        self.states = {"eat": hunger, "drink": thirst}
        self.hunger_rate = hunger_rate
        self.thirst_rate = thirst_rate
        self.tags = tags
        self.sounds = sounds
        self.lazyThreshold = lazyThreshold
        actorList.append(self)
