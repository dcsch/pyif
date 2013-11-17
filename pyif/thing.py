
from . import parser
from . import action
from . import grammar
from . import glk
from .debug import log

#from . import *

#####################################################################
# 'Constant' values
#####################################################################

# Attributes
#CLOTHING    = 1
#CONTAINER   = 2
#LIGHT       = 3
#OPEN        = 4
#SCENERY     = 5
#SUPPORTER   = 6
#TRANSPARENT = 7
#VISITED     = 8
#WORN        = 9

from . import CLOTHING, CONTAINER, LIGHT, OPEN, SCENERY, SUPPORTER, TRANSPARENT, VISITED, WORN

#####################################################################
# Story Object functions
#####################################################################

def move(obj, dest):
    "Move an object to be a child of the destination object."

    if obj not in dest.children:

        # Remove from current parent
        if obj.parent:
            log("removing %s from %s" % (obj.name, obj.parent.name))
            obj.parent.children.remove(obj)
            
        # Add to new parent, and set it as the object's parent
        log("adding %s to %s" % (obj.name, dest.name))
        dest.children.append(obj)
        obj.parent = dest
        
    else:
        log("%s is already in %s" % (obj.name, dest.name))

#####################################################################
# Story Objects
#####################################################################

class Thing:
    """The base object for all story objects.
    
    This is where all the common definitions for story objects live, as well
    as the object heirarchy management methods.
    """

    def __init__(self, name, parent):
        self.attributes = set()
        self.name = name
        self.article = "a"
        self.nouns = []
        self.parent = parent
        self.children = []

        self.react_before = None
        self.before = None
        self.after = None
        self.react_after = None

        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

        # If we have no parent, the root becomes our parent by default, and add
        # ourself to our parent's children
#        if self.parent is None:
#            self.parent = root
        if self.parent is not None:
            self.parent.children.append(self)
            
    def in_scope(self, noun):
        """
        Search for the noun amoungst all the objects within scope.
        """
        
        # Are we the noun?
        if noun in self.nouns:
            return self

        # Are we holding the noun?
        for c in self.children:
            if c.in_scope(noun):
                return c
                
        # Are we a sibling or near sibling to the noun?
        for c in self.parent.children:
            if c.in_scope(noun):
                return c

        return None

    def has_light(self):
        if LIGHT in self.attributes:
            return True
        else:
            for c in self.children:
                if c.has_light():
                    return True
        return False

    def find(self, noun):
        for c in self.children:
            if noun in c.nouns:
                return c
            else:
                d = c.find(noun)
                if d:
                    return d
        return None
        
    def room(self):
        "The room that contains this thing, or self if it is a room"
        if isinstance(self, Room):
            return self
        else:
            return self.parent.room()
        
    def tree(self, indent=0):
        glk.put_string(" " * indent + self.name + "\n")
        for c in self.children:
            c.tree(indent + 1)

class Player(Thing):

    pass

class Room(Thing):

    pass
#    def __init__(self, name):
#        super.__init__(super, name)

class Scenery(Thing):
    pass

class Story:

    def __init__(self, name, headline, delegate):
        self.name = name
        self.headline = headline
        self.release = 1
        self.serial = 81001
        self.delegate = delegate
        
        self.root = Thing("root", None)
        
        self.compass = Thing("compass", self.root)
        self.north = Thing("north", self.compass)
        self.north.nouns = ["north"]
        self.east = Thing("east", self.compass)
        self.east.nouns = ["east"]
        self.south = Thing("south", self.compass)
        self.south.nouns = ["south"]
        self.west = Thing("west", self.compass)
        self.west.nouns = ["west"]
        self.northeast = Thing("northeast", self.compass)
        self.northeast.nouns = ["northeast"]
        self.northwest = Thing("northwest", self.compass)
        self.northwest.nouns = ["northwest"]
        self.southeast = Thing("southeast", self.compass)
        self.southeast.nouns = ["southeast"]
        self.southwest = Thing("southwest", self.compass)
        self.southwest.nouns = ["southwest"]
        self.up_above = Thing("up above", self.compass)
        self.up_above.nouns = ["up", "above"]
        self.ground = Thing("ground", self.compass)
        self.ground.nouns = ["ground"]
        self.inside = Thing("inside", self.compass)
        self.inside.nouns = ["inside"]
        self.outside = Thing("outside", self.compass)
        self.outside.nouns = ["outside"]

        # Player
        self.player = Player("cretin", self.root)
        self.player.nouns = ["cretin", "me"]
        self.player.description = "As good looking as ever."
        
        self.actor = self.player

        self.nouns = []
        
        # State and Parser
        self.has_quit = False
        self.deadflag = 0
        self.keep_silent = False

        self.grammar = grammar.Grammar(self)
        
        self.parser = parser.Parser(self, self.grammar)
        
        
    def run(self):
        "The main story loop"
        
        if self.delegate:
            self.delegate.initialise()

        # The initial text
        action.version(self)
        glk.put_char("\n")
        action.look(self, True)

#         while True:
#             event = glk.select()
#             if event.type == EVTYPE_LINEINPUT:
                
        
        while self.parser.read_input():
            if self.deadflag:
                self.handle_deadflag()
                
    def handle_deadflag(self):
        "Report the player's end-of-game status"
        glk.put_string("\n    *** ")
        handled = False
        if self.delegate and "death_message" in dir(self.delegate):
            handled = self.delegate.death_message()
        if not handled:
            self.death_message()
        glk.put_string(" ***\n\n\n")
        

    def death_message(self):
        "The text of the death message"
        if self.deadflag == 1:
            glk.put_string("You have died")
        elif self.deadflag == 2:
            glk.put_string("You have won")
        
                
    

#####################################################################
# Globals
#####################################################################

