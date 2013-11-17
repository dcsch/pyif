
from . import action
from .parser import NOUN_TOKEN, HELD_TOKEN, MULTI_TOKEN, MULTIHELD_TOKEN, MULTIEXCEPT_TOKEN, MULTIINSIDE_TOKEN, TOPIC_TOKEN, CREATURE_TOKEN
from .debug import log

#from . import *

class Verb:

    def __init__(self, grammar, verb_tokens):
        self.grammar = grammar
        self.verb_tokens = verb_tokens
        self.actions = []

    def add_action(self, tokens, action, nouns=None):
        self.actions.append((tokens, action, nouns))
        
    def find_action_matching_tokens(self, tokens):
        """
        Find an action defined by this verb that matches the given token pattern.
        Returns the matching action, and a list of matching noun tokens.
        """

        for a in self.actions:
        
            log(" examining action %s" % a[1])

            # Does the token count match?
            if len(tokens) != len(a[0]):
                continue

            # Try to match the tokens
            matched_noun_tokens = []
            match_count = 0
            for i in range(len(a[0])):
            
                # Is the token definition a tuple?  If so, the token type
                # is the first part, and a qualifying function the second
                if isinstance(a[0][i], tuple):
                    t = a[0][i][0]
                    f = a[0][i][1]
                else:
                    t = a[0][i]
                    f = None

                if t == NOUN_TOKEN or MULTI_TOKEN:
                    
                    # We are expecting a noun -- is it legal?
                    log("NOUN_TOKEN")
                    if self.grammar.legal_noun_token(tokens[i]):
                    
                        # Is there a qualifying function?
                        if f == None or f() == True:
                            log("matched noun token")
                            matched_noun_tokens.append((tokens[i], t))
                            match_count += 1
                        else:
                            log("noun token matched but qualifying function returned False")

                if t == HELD_TOKEN:
                    
                    # We are expecting a noun -- is it legal?
                    log("HELD_TOKEN")
                    if self.grammar.legal_noun_token(tokens[i]):
                        log("matched noun token")
                        matched_noun_tokens.append((tokens[i], t))
                        match_count += 1

                elif t == tokens[i]:
                    log("matched: %s" % t)
                    match_count += 1
        
            if match_count == len(a[0]):
                return (a, matched_noun_tokens)
            
        return (None, None)
    

class Grammar:

    def __init__(self, story):
        self.story = story
        self.verbs = []
#        self.nouns = []

        # Meta-verbs
        verb = self.add_verb(["brief", "normal"])
        verb.add_action([], action.brief)

        verb = self.add_verb(["verbose", "long"])
        verb.add_action([], action.verbose)

        verb = self.add_verb(["superbrief", "short"])
        verb.add_action([], action.superbrief)

        verb = self.add_verb(["quit", "q", "die"])
        verb.add_action([], action.quit)

        verb = self.add_verb(["restart"])
        verb.add_action([], action.restart)

        verb = self.add_verb(["restore"])
        verb.add_action([], action.restore)

        verb = self.add_verb(["save"])
        verb.add_action([], action.save)

        verb = self.add_verb(["score"])
        verb.add_action([], action.score)

        verb = self.add_verb(["version"])
        verb.add_action([], action.version)

        # Game Verbs
        verb = self.add_verb(["answer", "say", "shout", "speak"])
        verb.add_action([TOPIC_TOKEN, "to", CREATURE_TOKEN], action.answer)

        verb = self.add_verb(["ask"])
        verb.add_action([CREATURE_TOKEN, "about", TOPIC_TOKEN], action.ask)
        verb.add_action([CREATURE_TOKEN, "for", NOUN_TOKEN], action.ask_for)
        verb.add_action([CREATURE_TOKEN, "to", TOPIC_TOKEN], action.ask_to)
        verb.add_action(["that", CREATURE_TOKEN, TOPIC_TOKEN], action.ask_to)

        verb = self.add_verb(["attack", "break", "crack", "destroy",
            "fight", "hit", "kill", "murder", "punch",
            "smash", "thump", "torture", "wreck"])
        verb.add_action([NOUN_TOKEN], action.attack)

        verb = self.add_verb(["blow"])
        verb.add_action([HELD_TOKEN], action.blow)

        verb = self.add_verb(["bother", "curses", "darn", "drat"])
        verb.add_action([], action.mild)
        verb.add_action([TOPIC_TOKEN], action.mild)

        verb = self.add_verb(["burn", "light"])
        verb.add_action([NOUN_TOKEN], action.burn)
        verb.add_action([NOUN_TOKEN, "with", HELD_TOKEN], action.burn)

        verb = self.add_verb(["buy", "purchase"])
        verb.add_action([NOUN_TOKEN], action.buy)

        verb = self.add_verb(["climb", "scale"])
        verb.add_action([NOUN_TOKEN], action.climb)
        verb.add_action(["up", NOUN_TOKEN], action.climb)
        verb.add_action(["over", NOUN_TOKEN], action.climb)

        verb = self.add_verb(["close", "cover", "shut"])
        verb.add_action([NOUN_TOKEN], action.close)
        verb.add_action(["up", NOUN_TOKEN], action.close)
        verb.add_action(["off", NOUN_TOKEN], action.switch_off)

        verb = self.add_verb(["consult"])
        verb.add_action([NOUN_TOKEN, "about", TOPIC_TOKEN], action.consult)
        verb.add_action([NOUN_TOKEN, "on", TOPIC_TOKEN], action.consult)

        verb = self.add_verb(["cut", "chop", "prune", "slice"])
        verb.add_action([NOUN_TOKEN], action.cut)

        verb = self.add_verb(["dig"])
        verb.add_action([NOUN_TOKEN], action.dig)
        verb.add_action([NOUN_TOKEN, "with", HELD_TOKEN], action.dig)

        verb = self.add_verb(["drink", "sip", "swallow"])
        verb.add_action([NOUN_TOKEN], action.drink)

        verb = self.add_verb(["drop", "discard", "throw"])
        verb.add_action([MULTIHELD_TOKEN], action.drop)
        verb.add_action([MULTIEXCEPT_TOKEN, "in", NOUN_TOKEN], action.insert)
        verb.add_action([MULTIEXCEPT_TOKEN, "into", NOUN_TOKEN], action.insert)
        verb.add_action([MULTIEXCEPT_TOKEN, "down", NOUN_TOKEN], action.insert)
        verb.add_action([MULTIEXCEPT_TOKEN, "on", NOUN_TOKEN], action.put_on)
        verb.add_action([MULTIEXCEPT_TOKEN, "onto", NOUN_TOKEN], action.put_on)
        verb.add_action([HELD_TOKEN, "at", NOUN_TOKEN], action.throw_at)
        verb.add_action([HELD_TOKEN, "against", NOUN_TOKEN], action.throw_at)
        verb.add_action([HELD_TOKEN, "on", NOUN_TOKEN], action.throw_at)
        verb.add_action([HELD_TOKEN, "onto", NOUN_TOKEN], action.throw_at)

        verb = self.add_verb(["eat"])
        verb.add_action([HELD_TOKEN], action.eat)

        verb = self.add_verb(["empty"])
        verb.add_action([NOUN_TOKEN], action.empty)
        verb.add_action(["out", NOUN_TOKEN], action.empty)
        verb.add_action([NOUN_TOKEN, "out"], action.empty)
        verb.add_action([NOUN_TOKEN, "to", NOUN_TOKEN], action.empty_to)
        verb.add_action([NOUN_TOKEN, "into", NOUN_TOKEN], action.empty_to)
        verb.add_action([NOUN_TOKEN, "on", NOUN_TOKEN], action.empty_to)
        verb.add_action([NOUN_TOKEN, "onto", NOUN_TOKEN], action.empty_to)

        verb = self.add_verb(["enter", "cross"])
        verb.add_action([], action.go_in)
        verb.add_action([NOUN_TOKEN], action.enter)

#        verb = self.add_verb(["examine", "x", "read"])
        verb = self.add_verb(["examine", "x", "check", "describe", "watch"])
        verb.add_action([NOUN_TOKEN], action.examine)

        verb = self.add_verb(["exit", "out", "outside"])
        verb.add_action([], action.exit)
        verb.add_action([NOUN_TOKEN], action.exit)

        verb = self.add_verb(["fill"])
        verb.add_action([NOUN_TOKEN], action.fill)
        
        verb = self.add_verb(["get"])
        verb.add_action(["out"], action.exit)
        verb.add_action(["off"], action.exit)
        verb.add_action(["up"], action.exit)
        verb.add_action([MULTI_TOKEN], action.take)
        verb.add_action(["in", NOUN_TOKEN], action.enter)
        verb.add_action(["into", NOUN_TOKEN], action.enter)
        verb.add_action(["on", NOUN_TOKEN], action.enter)
        verb.add_action(["onto", NOUN_TOKEN], action.enter)
        verb.add_action(["off", NOUN_TOKEN], action.get_off)
        verb.add_action([MULTIINSIDE_TOKEN, "from", NOUN_TOKEN], action.remove)

        verb = self.add_verb(["give", "feed", "offer", "pay"])
        verb.add_action([HELD_TOKEN, "to", CREATURE_TOKEN], action.give)
        verb.add_action(["over", HELD_TOKEN, "to", CREATURE_TOKEN], action.give)
        verb.add_action([CREATURE_TOKEN, HELD_TOKEN], action.give)  # TODO reverse the tokens
        
        verb = self.add_verb(["go", "run", "walk"])
        verb.add_action([], action.vague_go)
        verb.add_action([(NOUN_TOKEN, self.is_direction)], action.go)

        verb = self.add_verb(["inventory", "inv", "i"])
        verb.add_action([], action.inventory)

        verb = self.add_verb(["look", "l"])
        verb.add_action([], action.look)
        verb.add_action(["at", NOUN_TOKEN], action.examine)

        verb = self.add_verb(["put"])
        verb.add_action([HELD_TOKEN, "on", NOUN_TOKEN], action.put_on)
        verb.add_action(["on", HELD_TOKEN], action.wear)

        verb = self.add_verb(["search"])
        verb.add_action([NOUN_TOKEN], action.search)

        verb = self.add_verb(["take", "get"])
        verb.add_action([NOUN_TOKEN], action.take)
        verb.add_action(["off", NOUN_TOKEN], action.disrobe)

        verb = self.add_verb(["wear", "don"])
        verb.add_action([HELD_TOKEN], action.wear)



        # Directions
        verb = self.add_verb(["north", "n"])
        verb.add_action([], action.go, [self.story.north])

        verb = self.add_verb(["east", "e"])
        verb.add_action([], action.go, [self.story.east])

        verb = self.add_verb(["south", "s"])
        verb.add_action([], action.go, [self.story.south])

        verb = self.add_verb(["west", "w"])
        verb.add_action([], action.go, [self.story.west])

        verb = self.add_verb(["northeast", "ne"])
        verb.add_action([], action.go, [self.story.northeast])

        verb = self.add_verb(["northwest", "nw"])
        verb.add_action([], action.go, [self.story.northwest])

        verb = self.add_verb(["southeast", "se"])
        verb.add_action([], action.go, [self.story.southeast])

        verb = self.add_verb(["southwest", "sw"])
        verb.add_action([], action.go, [self.story.southwest])

        verb = self.add_verb(["up", "u"])
        verb.add_action([], action.go, [self.story.up_above])

        verb = self.add_verb(["down", "d"])
        verb.add_action([], action.go, [self.story.ground])

        verb = self.add_verb(["in"])
        verb.add_action([], action.go, [self.story.inside])

        verb = self.add_verb(["out"])
        verb.add_action([], action.go, [self.story.outside])


        # Debugging verbs
        verb = self.add_verb(["actions"])
        verb.add_action([], action.actions)

        verb = self.add_verb(["grammar"])
        verb.add_action([], action.grammar)
        
        verb = self.add_verb(["messages"])
        verb.add_action([], action.messages)

        verb = self.add_verb(["tree"])
        verb.add_action([], action.tree)
        
        verb = self.add_verb(["dump"])
        verb.add_action([NOUN_TOKEN], action.dump)
        
    def add_verb(self, verb_tokens):
        verb = Verb(self, verb_tokens)
        self.verbs.append(verb)
        return verb

    def find_verb_matching_token(self, token):
        for verb in self.verbs:
            if token in verb.verb_tokens:
                return verb
        return None
        
    def legal_noun_token(self, noun_token):
        "Is this noun token legal?  Does it exist somewhere in the story?"
        n = self.story.root.find(noun_token)
        if n:
            return True
        else:
            return False
            
    def is_direction(self):
        return True
