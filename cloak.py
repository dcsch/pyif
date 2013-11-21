###############################################################################
# Cloak of Darkness - a simple demonstration of Interactive Fiction
# Python version, using PyIF, written by David Schweinsberg
###############################################################################

from pyif.story import Story
from pyif import thing
from pyif import parser
from pyif import action
from pyif import util
from pyif import glk

class Delegate:

    def initialise(self):

        thing.move(story.player, foyer)

        glk.put_string("\n\nHurrying through the rainswept November night, you're glad to see the \
bright lights of the Opera House. It's surprising that there aren't more \
people about but, hey, what do you expect in a cheap demo game...?\n\n\n")

    def death_message(self):
        if story.deadflag == 3:
            glk.put_string("You have lost")
            return True
        return False
    
story = Story("Cloak of Darkness", "A basic IF demonstration.", Delegate())

###############################################################################
# Rooms
###############################################################################

foyer = thing.Room("Foyer of the Opera House", story.root)
foyer.nouns = ["foyer"]
foyer.description = util.cw("""
You are standing in a spacious hall, splendidly decorated in red
and gold, with glittering chandeliers overhead. The entrance from
the street is to the north, and there are doorways south and west.
""")
foyer.attributes.add(thing.LIGHT)

bar = thing.Room("Foyer bar", story.root)
bar.nouns = ["bar"]
bar.description = util.cw("""
The bar, much rougher than you'd have guessed after the opulence
of the foyer to the north, is completely empty. There seems to
be some sort of message scrawled in the sawdust on the floor.
""")
def bar_before(self, story):
    if story.action is action.go:
        if thing.LIGHT not in self.attributes and story.nouns[0] is not story.north:
            message.number += 2
            glk.put_string("Blundering around in the dark isn't a good idea!\n")
            return True
    else:
        if thing.LIGHT not in self.attributes:
            message.number += 1
            glk.put_string("In the dark? You could easily disturb something!\n")
            return True
    return False
bar.before = bar_before

message = thing.Thing("scrawled message", bar)
message.nouns = ["message", "sawdust", "floor"]
def message_description(self):
    if self.number < 2:
        story.deadflag = 2
        glk.put_string("The message, neatly marked in the sawdust, reads...\n")
    else:
        story.deadflag = 3
        glk.put_string("The message has been carelessly trampled, making it \
difficult to read. You can just distinguish the words...\n")
message.description = message_description
message.number = 0
message.attributes.add(thing.SCENERY)

cloakroom = thing.Room("Cloakroom", story.root)
cloakroom.nouns = ["cloakroom"]
cloakroom.description = util.cw("""
The walls of this small room were clearly once lined with hooks,
though now only one remains. The exit is a door to the east.
""")
cloakroom.attributes.add(thing.LIGHT)

hook = thing.Thing("small brass hook", cloakroom)
hook.nouns = ["small", "brass", "hook", "peg"]
def hook_description(self):
    glk.put_string("It's just a small brass hook, ")
    if self is cloak.parent:
        glk.put_string("with a cloak hanging on it.\n")
    else:
        glk.put_string("screwed to the wall.\n")
hook.description = hook_description
hook.attributes.add(thing.SCENERY)
hook.attributes.add(thing.SUPPORTER)


###############################################################################
# Connections
###############################################################################

foyer.s_to = bar
foyer.w_to = cloakroom
foyer.n_to = "You've only just arrived, and besides, the weather outside seems to be getting worse."

bar.n_to = foyer

cloakroom.e_to = foyer

cloak = thing.Thing("velvet cloak", story.player)
cloak.nouns = ["handsome", "dark", "black", "velvet", "satin", "cloak"]
cloak.description = util.cw("""
A handsome cloak, of velvet trimmed with satin, and slightly
spattered with raindrops. Its blackness is so deep that it
almost seems to suck light from the room.
""")
def cloak_before(self, story):
    if story.action is action.drop or story.action is action.put_on:
        if story.actor.room() is cloakroom:
            bar.attributes.add(thing.LIGHT)
            return False
        else:
            glk.put_string("This isn't the best place to leave a smart cloak lying around.\n")
            return True
    return False
cloak.before = cloak_before
def cloak_after(self, story):
    if story.action is action.take:
        bar.attributes.discard(thing.LIGHT)
    return False
cloak.after = cloak_after
cloak.attributes.add(thing.CLOTHING)
cloak.attributes.add(thing.WORN)

t1 = thing.Thing("foo", foyer)
t1.nouns = ["foo"]
t1.description = "A simple foo."

t2 = thing.Thing("bar", foyer)
t2.nouns = ["bar"]
t2.description = "A simple bar."

###############################################################################
# Grammar
###############################################################################

verb = story.grammar.add_verb(["hang"])
verb.add_action([parser.HELD_TOKEN, "on", parser.NOUN_TOKEN], action.put_on)

###############################################################################
# Start up
###############################################################################

def glk_main():
    story.run()

glk.main(glk_main)
