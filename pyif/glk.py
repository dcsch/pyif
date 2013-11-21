
import curses
#from . import util

# Constants

STYLE_NORMAL       = 1
STYLE_EMPHASIZED   = 2
STYLE_PREFORMATTED = 3
STYLE_HEADER       = 4
STYLE_SUBHEADER    = 5

EVTYPE_NONE        = 0
EVTYPE_TIMER       = 1
EVTYPE_CHARINPUT   = 2
EVTYPE_LINEINPUT   = 3
EVTYPE_MOUSEINPUT  = 4
EVTYPE_ARRANGE     = 5
EVTYPE_REDRAW      = 6
EVTYPE_HYPERLINK   = 7

# Globals

stdscr = None
line_history = []

# Classes

class Event:
    
    def __init__(self, event_type):
        self.event_type = event_type
        self.win = None
        self.val1 = 0
        self.val2 = 0

# Functions

def main(glk_main):
    curses.wrapper(curses_main, glk_main)
    
def curses_main(wrapper_stdscr, glk_main):
    global stdscr
    stdscr = wrapper_stdscr
    stdscr.idlok(1)
    stdscr.scrollok(1)
    
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    glk_main()

    maxyx = stdscr.getmaxyx()
    stdscr.addstr(maxyx[0] - 1, 1, "Hit any key to exit.", curses.color_pair(1))
    stdscr.getch()

def put_char(char):
    #stdscr.addch(char)
    stdscr.addstr(char)
    stdscr.refresh()
    
def put_string(string):
#     height, width = stdscr.getmaxyx()
#     string_with_breaks = util.insert_newlines(string, width)
#     stdscr.addstr(string_with_breaks)
    stdscr.addstr(string)
    stdscr.refresh()
    
def set_style(style):
    if style == STYLE_NORMAL:
        attr = curses.A_NORMAL
    elif style == STYLE_EMPHASIZED:
        attr = curses.A_STANDOUT
    elif style == STYLE_PREFORMATTED:
        attr = curses.A_NORMAL
    elif style == STYLE_HEADER:
        attr = curses.A_BOLD
    elif style == STYLE_SUBHEADER:
        attr = curses.A_BOLD
    stdscr.attrset(attr)

def get_string():
    s = ""
    pos = 0
    anchor = stdscr.getyx()

    global line_history
    line_history.append(s)
    line_history_pos = len(line_history) - 1

    while True:
        c = stdscr.getch()
        #stdscr.addstr("%d" % c)
        if c == 10:
        
            # Return / Linefeed
            stdscr.addch(anchor[0], anchor[1] + len(s), 60)
            stdscr.addch(c)
            break

        elif c == 127:
        
            # Delete
            if pos:
                pos -= 1
                s = s[:pos] + s[pos + 1:]
                stdscr.move(anchor[0], anchor[1])
                stdscr.clrtobot()
                stdscr.addstr(anchor[0], anchor[1], s)
                stdscr.move(anchor[0], anchor[1] + pos)
                
        elif c == curses.KEY_LEFT:
        
            if pos:
                pos -= 1
                stdscr.move(anchor[0], anchor[1] + pos)

        elif c == curses.KEY_RIGHT:
        
            if pos < len(s):
                pos += 1
                stdscr.move(anchor[0], anchor[1] + pos)

        elif c == curses.KEY_UP:
        
            if line_history_pos:
                line_history_pos -= 1
                s = line_history[line_history_pos]
                pos = len(s)
                stdscr.move(anchor[0], anchor[1])
                stdscr.clrtobot()
                stdscr.addstr(anchor[0], anchor[1], s)
                stdscr.move(anchor[0], anchor[1] + pos)

        elif c == curses.KEY_DOWN:
        
            if line_history_pos < len(line_history) - 1:
                line_history_pos += 1
                s = line_history[line_history_pos]
                pos = len(s)
                stdscr.move(anchor[0], anchor[1])
                stdscr.clrtobot()
                stdscr.addstr(anchor[0], anchor[1], s)
                stdscr.move(anchor[0], anchor[1] + pos)

        elif c < curses.KEY_MIN:
        
            # Treat this as a printable character
            s = s[:pos] + "%c" % c + s[pos:]
            pos += 1
            stdscr.addstr(anchor[0], anchor[1], s)
            stdscr.move(anchor[0], anchor[1] + pos)

            # Set the line history
            line_history = line_history[:-1]
            line_history.append(s)
    
            # Debugging
            #stdscr.addstr(50, 0, "%s" % line_history)
            #stdscr.move(anchor[0], anchor[1] + pos)

    # Update the line history
    line_history = line_history[:-1]
    line_history.append(s)

    return s
