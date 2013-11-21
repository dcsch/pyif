
def is_whitespace(c):
    if c == " " or c == "\t" or c == "\n":
        return True
    return False

def compress_whitespace(s):
    """
    Remove extraneous whitespace from the string, that being all whitespace at the beginning
    and end of the string and anything beyond a single space within the string.
    """
    
    new_str = ""
    in_text = False
    for i in range(len(s)):
        c = s[i]
        if is_whitespace(c):
            if not in_text:

                # Before any text, so ignore
                pass
            else:

                # We're leaving text, so we allow one space and ignore all others
                new_str += " "
                in_text = False
        else:
            # Handling text
            new_str += c
            in_text = True
    if new_str[-1:] == " ":
        new_str = new_str[:-1]
    return new_str

def cw(s):
    return compress_whitespace(s)

def insert_newlines(s, width):
    """
    Insert newlines into the string so words don't wrap at the end of lines.
    """
    
    new_str = ""
    
    # Jump to the end of a line and scan backwards for whitespace
    start = 0
    pos = width
    while pos < len(s):
        for i in range(pos, pos - width, -1):
            if is_whitespace(s[i]):
                for j in range(i - 1, pos - width, -1):
                    if not is_whitespace(s[j]):
                        i = j + 1
                new_str += s[start:i + 1] + "\n"
                start = i + 1
                pos += width
                break
    if start < len(s):
        new_str += s[start:]
    return new_str
