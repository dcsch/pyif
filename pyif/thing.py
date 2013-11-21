
from . import glk
from .debug import log

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
        
                
    

#####################################################################
# Globals
#####################################################################

