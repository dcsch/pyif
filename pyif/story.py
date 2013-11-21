'''
Created on Nov 21, 2013

@author: david
'''

from thing import Thing, Player
import grammar
import parser
import action
import glk

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
