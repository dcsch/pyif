
#from . import action
from . import glk
from . import message
from .debug import log

#from . import *

NOUN_TOKEN        = 1
HELD_TOKEN        = 2
MULTI_TOKEN       = 3
MULTIHELD_TOKEN   = 4
MULTIEXCEPT_TOKEN = 5
MULTIINSIDE_TOKEN = 6
TOPIC_TOKEN       = 7
CREATURE_TOKEN    = 8

def tokenise_string(string):
    "Transform the string into a list of tokens"
    tokens = []
    start = 0
    for i in range(len(string)):
        if string[i] == " ":
            if start < i:
                tokens.append(string[start:i])
            start = i + 1
    if len(string) > 0 and start <= i:
        tokens.append(string[start:i + 1])
    return tokens

class Parser:
    """Inputs commands from the user and executes them.
    
    At the moment this is very simple -- just enough to get us going.
    """
    
    def __init__(self, story, grammar):
        self.story = story
        self.grammar = grammar
        
    def read_input(self):
        """
        Parser strategy:
        * Break input into tokens
        * Match the initial token with a verb definition in the grammar
        """

        glk.put_string("\n>")
        line = glk.get_string()
        tokens = tokenise_string(line)
        
        if len(tokens) == 0:
            glk.put_string(message.PARDON);
            return True

        # Make the actor always the player for the moment
        self.story.actor = self.story.player
        
        # Find the Verb that handles this
        verb = self.grammar.find_verb_matching_token(tokens[0])
        if verb:
            log("matched: " + tokens[0])
            
            a, noun_tokens_and_types = verb.find_action_matching_tokens(tokens[1:])
            
            if a:
                log("ACTION: %s, MATCHED NOUNS: %s" % (a[1], noun_tokens_and_types))
                
                matched_nouns = []
                for noun_token, noun_type in noun_tokens_and_types:
                    n = self.ensure_noun_token_in_scope(noun_token, noun_type)
                    if not n:
                        glk.put_string(message.CANT_SEE_A % noun_token)
                        return True
                    matched_nouns.append(n)

                self.story.action = a[1]
                self.story.nouns = matched_nouns

                # Substitute nouns if we have them (e.g. directions)
                if a[2]:
                    self.story.nouns = a[2]

                # Execute the action
                a[1](self.story)

                return not self.story.has_quit
            else:
                log("NO ACTION MATCH")

            glk.put_string(message.UNDERSTAND_AS_FAR % verb.verb_tokens[0])
            return True

        glk.put_string(message.NOT_A_VERB)
        return True
            
    def ensure_noun_token_in_scope(self, noun_token, noun_type):

        room = self.story.player.room()
        n = None
        
        # If the noun type is 'HELD_TOKEN', are we holding the noun?
        if noun_type == HELD_TOKEN:
            n = self.story.actor.find(noun_token)
            
            # If we're not holding it, so can we see it to do an implicit take?
            if not n:
                n = room.find(noun_token)
                if n:
                    self.story.nouns = [n]
                    glk.put_string(message.FIRST_TAKING % (n.article, n.name))
                    ks = self.story.keep_silent
                    self.story.keep_silent = True
                    action.take(self.story)
                    self.story.keep_silent = ks
                    n = self.story.actor.find(noun_token)
                
        elif noun_type == NOUN_TOKEN:
            n = room.find(noun_token)

        if n:
            log("matched noun: " + n.name)
            return n

        return None
