
# Default verb actions

#from . import thing
from . import glk
from . import message
from .debug import log
#from types import *

from . import CLOTHING, CONTAINER, LIGHT, OPEN, SCENERY, SUPPORTER, TRANSPARENT, VISITED, WORN

#from . import *

def before_actions(story):

    room = story.actor.room()

    # Call 'react_before' on all objects in scope
    for item in room.children:
        if item.react_before:
            log("'%s'.react_before()" % item.name)
            if item.react_before(item, story):
                return True
    
    # Call 'before' of the current room
    log("'%s'.before()" % room.name)
    if room.before:
        if room.before(room, story):
            return True
    
    # Call before of the first noun if there is one
    if len(story.nouns) > 0 and story.nouns[0].before:
        log("'%s'.before()" % story.nouns[0].name)
        if story.nouns[0].before(story.nouns[0], story):
            return True
            
    return False

def after_actions(story):

    room = story.actor.room()

    # Call 'react_after' on all objects in scope
    for item in room.children:
        if item.react_after:
            log("'%s'.react_after()" % item.name)
            if item.react_after(item, story):
                return True
    
    # Call 'after' of the current room
    log("'%s'.after()" % room.name)
    if room.after:
        if room.after(room, story):
            return True
    
    # Call after of the first noun if there is one
    if len(story.nouns) > 0 and story.nouns[0].after:
        log("'%s'.after()" % story.nouns[0].name)
        if story.nouns[0].after(story.nouns[0], story):
            return True
            
    return False

def brief(story):
    "Switch to brief (normal) descriptions"
    
    return False

def verbose(story):
    "Switch to verbose (long) descriptions"
    
    return False

def superbrief(story):
    "Switch to superbrief (short) descriptions"
    
    return False

def quit(story):
    "End the story."

    story.has_quit = True

def restart(story):
    pass

def restore(story):
    pass

def save(story):
    pass
    
def score(story):
    pass
    
def version(story):
    glk.set_style(glk.STYLE_HEADER)
    glk.put_string(story.name)
    glk.put_char("\n")
    glk.set_style(glk.STYLE_NORMAL)
    glk.put_string(story.headline)
    glk.put_char("\n")
    glk.put_string("Release %d / Serial number %06d / PyIF 1.0a1\n" % (story.release, story.serial))
    
def answer(story):
    pass

def ask(story):
    pass

def ask_for(story):
    pass

def ask_to(story):
    pass

def attack(story):
    pass

def blow(story):
    pass
    
def burn(story):
    pass

def buy(story):
    pass

def climb(story):
    pass

def close(story):
    pass

def consult(story):
    pass

def cut(story):
    pass

def dig(story):
    pass

def drink(story):
    pass

def drop(story):
    "Drop an item."
    
    if before_actions(story):
        return

    # First check if it is being worn
    if WORN in story.nouns[0].attributes:
        glk.put_string(message.FIRST_TAKING_OFF % story.nouns[0].name)
        if not disrobe(story):
            return

    thing.move(story.nouns[0], story.actor.room())
    if after_actions(story):
        return
    if not story.keep_silent:
        glk.put_string(message.DROPPED)

def eat(story):
    pass

def empty(story):
    pass

def empty_to(story):
    pass

def enter(story):
    pass

def examine(story):
    "Print a description of the examined object"

    if before_actions(story):
        return

    # Is there a light source to see by?
    if not story.actor.room().has_light():
        glk.put_string(message.TOO_DARK)
        return

    if isinstance(story.nouns[0].description, str):
        glk.put_string(story.nouns[0].description)
        glk.put_char("\n")
    elif isinstance(story.nouns[0].description, FunctionType):
        story.nouns[0].description(story.nouns[0])

def exit(story):
    pass

def fill(story):
    pass

def fill(story):
    pass

def get_off(story):
    pass

def give(story):
    pass

def go_in(story):
    pass

def insert(story):
    pass

def inventory(story):
    "Print the items carried or worn by the player"
    
    if before_actions(story):
        return

    items = story.actor.children
    if len(items) == 0:
        glk.put_string(message.CARRYING_NOTHING)
    else:
        glk.put_string(message.CARRYING)
        for t in items:
            glk.put_string(" %s %s" % (t.article, t.name))
            if WORN in t.attributes:
                glk.put_string(message.BEING_WORN)
            else:
                glk.put_string("\n")

def look(story, implicit_look=False):
    "Print a description of the observer's location"

    # Don't execute before actions if this is an implicit look
    if not implicit_look:
        if before_actions(story):
            return

    room = story.actor.room()

    # Is there a light source to see by?
    if room.has_light():
        glk.set_style(glk.STYLE_SUBHEADER)
        glk.put_string(room.name)
        glk.put_char("\n")
        glk.set_style(glk.STYLE_NORMAL)

        if not implicit_look or VISITED not in room.attributes:
            glk.put_string(room.description)
            glk.put_char("\n")
            
        room.attributes.add(VISITED)
        
        # What objects can be seen here?
        str = content_description(story, room)
        if len(str):
            glk.put_char("\n")
            glk.put_string(message.CAN_SEE % str)

    else:
        # There is an issue here with the VISITED attribute.  Ideally, we should only see the
        # description if the room hasn't been visited, but if we set the VISITED attribute now,
        # and a light source is subsequently brought into the room, the description won't be output
        glk.set_style(glk.STYLE_SUBHEADER)
        glk.put_string(message.DARKNESS)
        glk.set_style(glk.STYLE_NORMAL)
        glk.put_string(message.DARKNESS_DESC)
        
def content_description(story, container):
    seen = []
    for obj in container.children:
        if obj is story.actor:
            continue
        if SCENERY in obj.attributes:
            continue
        seen.append(obj)
    count = len(seen)
    str = ""
    if count > 0:
        for obj in seen:
            str += "%s %s" % (obj.article, obj.name)
            
            if LIGHT in obj.attributes:
                str += " (" + message.PROVIDING_LIGHT + ")"
            
            if CONTAINER in obj.attributes:
                if OPEN in obj.attributes or TRANSPARENT in obj.attributes:
                    str2 = content_description(story, obj)
                    if len(str2):
                        str += " (" + message.IN_WHICH + str2 + ")"
            elif SUPPORTER in obj.attributes:
                str2 = content_description(story, obj)
                if len(str2):
                    str += " (" + message.ON_WHICH + str2 + ")"
            count -= 1
            if count > 1:
                str += ", "
            elif count > 0:
                str += message.AND
    return str

def mild(story):
    pass

def put_on(story):
    "Put an item in or on another item"
    
    if before_actions(story):
        return

    if SUPPORTER not in story.nouns[1].attributes:
        glk.put_string(message.CANT_PUT_ON % story.nouns[1].name)
        return

    # First check if it is being worn
    if WORN in story.nouns[0].attributes:
        glk.put_string(message.FIRST_TAKING_OFF % story.nouns[0].name)
        disrobe(story)
        if WORN in story.nouns[0].attributes:
            return

    thing.move(story.nouns[0], story.nouns[1])
    if after_actions(story):
        return
    glk.put_string(message.PUT_ON % (story.nouns[0].name, story.nouns[1].name))

def remove(story):
    pass

def switch_off(story):
    pass

def throw_at(story):
    pass

def go(story):
    "Simple movement"
    
    room = story.actor.room()
    
    if before_actions(story):
        return

    dest = None
    if story.nouns[0] == story.north:
        dest = room.n_to
    elif story.nouns[0] == story.south:
        dest = room.s_to
    elif story.nouns[0] == story.east:
        dest = room.e_to
    elif story.nouns[0] == story.west:
        dest = room.w_to
    if dest is not None:
        if isinstance(dest, str):
            glk.put_string(dest)
            glk.put_char("\n")
        else:
            log("%s going %s to %s" % (story.actor.name, story.nouns[0].name, dest.name))
            thing.move(story.actor, dest)
            if after_actions(story):
                return
            look(story, True)
    else:
        glk.put_string(message.CANT_GO)

def vague_go(story):
    pass

def search(story):
    "Search an item.  If a supporter or container, display the list of contents."

    room = story.actor.room()

    if before_actions(story):
        return

    # Is there a light source to see by?
    if not story.actor.room().has_light():
        glk.put_string(message.TOO_DARK)
        return

    str = content_description(story, story.nouns[0])
    if len(str):
        if CONTAINER in story.nouns[0].attributes:
            glk.put_string(message.IN)
        elif SUPPORTER in story.nouns[0].attributes:
            glk.put_string(message.ON)
        glk.put_string("the %s is %s.\n" % (story.nouns[0].name, str))
    else:
        glk.put_string("You find nothing of interest.\n")

def wear(story):
    "Put on an item of clothing."

    if before_actions(story):
        return

    if CLOTHING not in story.nouns[0].attributes:
        glk.put_string(message.CANT_WEAR)
        return

    if WORN in story.nouns[0].attributes:
        glk.put_string(message.ALREADY_WEARING)
        return

    story.nouns[0].attributes.add(WORN)
    if after_actions(story):
        return
    glk.put_string(message.WORN % story.nouns[0].name)

def take(story):
    "Take an item."

    if before_actions(story):
        return

    # We can't take sceney items, as they never appear in the list of visible
    # objects
    if SCENERY in story.nouns[0].attributes:
        glk.put_string(message.CANT_TAKE)
        return False
        
    thing.move(story.nouns[0], story.actor)
    if after_actions(story):
        return
    if not story.keep_silent:
        glk.put_string(message.TAKEN)
    return True

def disrobe(story):
    "Take off an item of clothing."

    if before_actions(story):
        return

    if WORN not in story.nouns[0].attributes:
        glk.put_string(message.NOT_WEARING)
        return False

    story.nouns[0].attributes.remove(WORN)
    if after_actions(story):
        return
    glk.put_string(message.DISROBE % story.nouns[0].name)
    return True

# Debugging verbs

def actions(story):
    story.debug_actions = True

def grammar(story):
    for verb in story.parser.grammar_obj.verbs:
        glk.put_string("%s\n" % verb)

def messages(story):
    story.debug_messages = True

def tree(story):
    story.root.tree()

def dump(story):
    glk.put_string("%s\n" % story.nouns[0].name)
    glk.put_string(" room: %s\n" % story.nouns[0].room().name)
