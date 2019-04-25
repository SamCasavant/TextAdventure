class Thing:
    def __init__(self, name, description=False, location=0, tags=[], eat_val=4):
        self.name = name
        if description:
            self.description = description
        else:
            self.description = name
        self.tags = tags
        self.eat_val = eat_val
        self.location = location
        if location:
            location.addThings([self])

    def lookAt(
        self
    ):  # Broken due to thing having .name and actor having .propername; will probably do away with proper/common name
        print(self.name)
        if self.name != self.description:
            print(self.description)
        for tag in self.tags:
            if tag in ["eat", "take", "drink"]:
                print(f"I can {tag} this.")
            elif tag in ["take_req"]:
                print("I have to have this in my inventory to use it.")
            elif tag in ["hungry", "thirsty"]:
                print(f"It looks {tag}.")


class Door(Thing):
    def __init__(
        self,
        name,
        connection,
        description=False,
        location=0,
        tags=["door", "openable", "pickable"],
        key=False,
        lockable=True,
        locked=False,
        closed=True,
    ):
        super(Door, self).__init__(name, description, location, tags, eat_val=0)
        self.tags = tags
        self.lockable = lockable
        self.locked = locked
        self.closed = closed
        self.connection = connection
        if lockable:
            if key:
                self.key = key
            else:
                print("Initialization Error: Lockable doors require a key.")
        if self.closed:
            connection.block("The door is closed.")

    def lock(self, key, actor):
        if not self.closed:
            return [
                0,
                [f"{actor.name} cannot lock an open door.", actor],
                actor.location,
            ]
        else:
            if self.lockable:
                if not self.locked:
                    self.locked = True

    def unlock(self, key, actor):
        if self.locked:
            if key == self.key:
                self.locked = False
            elif "pick" in key.tags:
                if "pickable" in self.tags:
                    self.locked = False
            else:
                print(f"{key.name} doesn't unlock this door.")
        else:
            print("This door is already unlocked.")

    def open(self, actor):
        if self.locked:
            if self.key in actor.inventory:
                print(f"I'll have to unlock it first with {self.key.name}")
            else:
                print(f"I'll need to unlock this door, but I don't have the key.")
        else:
            if self.closed:
                self.closed = False
                self.connection.unblock()
            else:
                print("This door is already open.")

    def close(self):
        if not self.closed:
            self.closed = True
            self.connection.block("The door is shut.")
        else:
            print("This door is already closed.")


class Container(Thing):
    def __init__(
        self,
        name,
        contents=[],
        description=False,
        location=0,
        tags=["container", "pickable"],
        key=False,
        lockable=True,
        locked=False,
        closed=True,
    ):
        super(Container, self).__init__(name, description, location, tags, eat_val=0)
        self.contents = contents
        for item in self.contents:
            item.tags.append("contained")
        self.tags = tags
        self.lockable = lockable
        self.locked = locked
        self.closed = closed
        if lockable:
            if key:
                self.key = key
            else:
                print("Initialization Error: Lockable containers require a key.")

    def lock(self, key, actor):
        if self.lockable:
            if not self.locked:
                if self.closed:
                    self.locked = True
                else:
                    self.closed = True
                    self.locked = True

    def unlock(self, key, actor):
        if self.locked:
            if key == self.key:
                self.locked = False
            elif "pick" in key.tags:
                if "pickable" in self.tags:
                    self.locked = False
            else:
                print(f"{key.name} doesn't unlock this.")
        else:
            print("This is already unlocked.")

    def open(self, actor):
        if self.locked:
            if self.key in actor.inventory:
                print(f"I'll have to unlock it first with {self.key.name}")
            else:
                print(f"I'll need to unlock this, but I don't have the key.")
        else:
            if self.closed:
                self.closed = False
                print("Inside I find:")
                for thing in self.contents:
                    print(thing.name)
                    self.location.things.append(thing)
                else:
                    print("Nothing")
            else:
                print("This container is already open.")

    def withdraw(self, thing, actor):
        if thing in self.contents:
            if len(actor.inventory) < actor.max_inv:
                actor.inventory.append(thing)
                self.contents.remove(thing)
