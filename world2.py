import actors
import things
import space
from copy import copy
import chrono


def worldInit():
    # things
    pie = things.Thing("pie", "A freshly baked pie.", tags=["take", "eat"])
    knife = things.Thing("knife", "Sharp as all heck.", tags=["take"])

    # Actors
    GrumphTorgi = actors.Human("Grumph Torgi", "Grumph", "A villain!")
    SilbertHumperdinck = actors.Human(
        "Silbert Humperdinck", "Sil", "Looks like a respectable fellow."
    )
    GertyVanFleek = actors.Human(
        "Gerty Van Fleek", "Gerty", "An old pie woman of some sort.", inventory=[pie]
    )
    MelissaMansname = actors.Human("Melissa Mansname", "Mel", "Just wed; nee Forthod")
    UmbrellaDeVille = actors.Human(
        "Umbrella DeVille", "Ella", "Should be named deMaitreDe."
    )
    hungryCat = actors.HouseCat(
        properName="Hungry Cat",
        commonName="Cat",
        description="He looks like he has a big appetite.",
        hunger=15,
        hunger_rate=15,
    )
    neverHungryCat = actors.HouseCat(
        properName="Hungry Cat",
        commonName="Cat",
        description="He looks like he has a big appetite.",
        hunger=0,
        hunger_rate=0,
    )
    # Spaces
    Alley = space.Space("alley", "A dark alley.")
    Park = space.Space("park", "Look at this grass.")
    TorgiHome = space.Space(
        "Torgi Household", "The cluttered home of a man named Torgi."
    )
    MansnameHome = space.Space(
        "Mansname Household", "Wow! It's hard to come up with descriptions!"
    )
    VanFleekHome = space.Space("Van Fleek Household", "Reeks of pie.")
    Restaurant = space.Space("Barren Grille", "I hear they have great desert.")
    # Spaces -Connections
    space.Connection(TorgiHome, Park, "north", "south")
    space.Connection(TorgiHome, Restaurant, "west", "east")
    space.Connection(Restaurant, Park, "north", "south")
    space.Connection(Park, Alley, "north", "south")
    space.Connection(VanFleekHome, Alley, "west", "east")
    space.Connection(MansnameHome, Alley, "east", "west")
    # Spaces -things
    tempKnife = copy(knife)
    TorgiHome.addThings([tempKnife])
    Restaurant.addThings([copy(pie)])

    # Spaces -Actors
    TorgiHome.addActors([GrumphTorgi, SilbertHumperdinck])
    Restaurant.addActors([UmbrellaDeVille])
    VanFleekHome.addActors([GertyVanFleek])
    MansnameHome.addActors([MelissaMansname])
    Park.addActors([hungryCat, neverHungryCat])
    # Actors -Itinerary
    GrumphTorgi.addItinerary(
        [
            (36000, ["take", tempKnife]),
            (43200, ["move", Park]),
            (57600, ["move", Alley]),
        ]
    )
    # SilbertHumperdinck.addItinerary([(25200, 'wake up'), ()])
    # Player
    player = actors.User("User", location=Park)
    actors.player = player
    return player
