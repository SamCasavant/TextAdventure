import actors
import things
import space
from copy import copy
import species

def worldInit():
    #things
    pie = things.Thing("pie", "A freshly baked pie.", tags=['take', 'eat'])
    knife = things.Thing("knife", "Sharp as all heck.", tags=['take'])

    #Actors
    GrumphTorgi = species.Human("Grumph Torgi", "Grumph", "A villain!")
    SilbertHumperdinck = species.Human("Silbert Humperdinck", "Sil", "Looks like a respectable fellow.")
    GertyVanFleek = species.Human("Gerty Van Fleek", "Gerty", "An old pie woman of some sort.", inventory=[pie])
    MelissaMansname = species.Human("Melissa Mansname", "Mel", "Just wed; nee Forthod")
    UmbrellaDeVille = species.Human("Umbrella DeVille", "Ella", "Should be named deMaitreDe.")
    #Spaces
    Alley = space.Space("alley", "A dark alley.")
    Park = space.Space("park", "Look at this grass.")
    TorgiHome = space.Space("Torgi Household", "The cluttered home of a man named Torgi.")
    MansnameHome = space.Space("Mansname Household", "Wow! It's hard to come up with descriptions!")
    VanFleekHome = space.Space("Van Fleek Household", "Reeks of pie.")
    Restaurant = space.Space("Barren Grille", "I hear they have great desert.")
    #Spaces -Connections
    space.Connection(TorgiHome, Park, 'north', 'south')
    space.Connection(TorgiHome, Restaurant, 'west', 'east')
    space.Connection(Restaurant, Park, 'north', 'south')
    space.Connection(Park, Alley, 'north', 'south')
    space.Connection(VanFleekHome, Alley, 'west', 'east')
    space.Connection(MansnameHome, Alley, 'east', 'west')
    #Spaces -things
    TorgiHome.addThings([copy(knife)])
    Restaurant.addThings([copy(pie)])

    #Spaces -Actors
    TorgiHome.addActors([GrumphTorgi, SilbertHumperdinck])
    Restaurant.addActors([UmbrellaDeVille])
    VanFleekHome.addActors([GertyVanFleek])
    MansnameHome.addActors([MelissaMansname])

    #Player
    player = species.User("User", location = Park)
    actors.player = player
    return player