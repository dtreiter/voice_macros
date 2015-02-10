WORD_MACROS = {
  # typing characters and troublesome letters
  "enter": "\n",
  "equals": "=",
  "plus": "+",
  "-": "-",
  "hyphen": "-",
  "_": "_",
  "underscore": "_",
  "parentheses": "(",
  "smile": ")",
  "brace": "[",
  "square": "]",
  "currently": "{",
  "curly": "{",
  "squiggle": "}",
  "bracket": "<",
  "knows": ">",
  "nose": ">",
  "*": "*",
  "~": "~",
  "`": "`",
  "bang": "!",
  "at": "@",
  "pound": "#",
  "dollar": "$",
  "percent": "%",
  "^": "^",
  "carrot": "^",
  "caret": "^",
  "&": "&",
  "ampersand": "&",
  "star": "*",
  "question": "?",
  "yes": "\r",
  "space": " ",
  "backspace": "",
  "complete": "",
  "window": "",
  "multiplex": "",
  "extend": "",
  "tab": "\t",
  ",": ",",
  ":": ":",
  ";": ";",
  "quote": "\"",
  "quotes": "\"",
  "\"": "\"",
  "single quote": "'",
  "/": "/",
  "search": "/",
  "peanut": "\\",
  "\\": "\\",
  
  # alphabet corrections
  "hey": "a",
  "be":    "b",
  "bee":    "b",
  "see":  "c",
  "egg":     "e",
  "eat":     "e",
  "find":  "f",
  "fine":  "f",
  "joe":   "j",
  "down": "j",
  "up": "k",
  "mark": "m",
  "in": "n",
  "oh": "o",
  "paste":     "p",
  "pope":     "p",
  "are":    "r",
  "you":  "u",
  "the":   "v",
  "visual":   "v",
  "why":   "y",
  "zebra": "z",

  # numbers
  "zero": "0",
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",

  # useful shortcuts
  "edit": "vim "
  "internet": "w3m google.com\njjjjjj\t\n"
  "emacs": "emacs "
}

LETTER_MACROS = {
  # alphabet
  "a":    "a",
  "b":    "b",
  "c": "c",
  "d":    "d",
  "e":     "e",
  "f":  "f",
  "g":     "g",
  "h":    "h",
  "i":    "i",
  "k":     "k",
  "l":     "l",
  "m":     "m",
  "n": "n",
  "o":    "o",
  "p":    "p",
  "q":   "q",
  "r":    "r",
  "s":   "s",
  "t":    "t",
  "u":  "u",
  "v":  "v",
  "w":  "w",
  "x":     "x",
  "y":   "y",
  "z":     "z"
}

# macro functions
def underscore(text):
  output = "_".join(text.lower().split(" "))
  return output

def hyphen(text):
  output = "-".join(text.lower().split(" "))
  return output

def camel(text):
  output = ''.join(letter for letter in text.title() if letter.isalpha())
  return output[0].lower() + output[1:]

def double_quote(text):
  output = "\"" + text + "\""
  return output

def single_quote(text):
  output = "'" + text + "'"
  return output

MACRO_FUNCTIONS = {
  "lower": (lambda text: text.lower()),
  "upper": (lambda text: text.upper()),
  "capital": (lambda text: text.title()),
  "trim": (lambda text: text.strip()),
  "camel": camel,
  "hyphenate": hyphen,
  "underline": underscore,
  "put this\"": double_quote,
  "put this\'": single_quote,
  "say": (lambda text: text)
}

# simple macros (ie. list -> ls)
#  # terminal
#  "list": "ls",
#  "change": "cd ",
#  "print me": "pwd",
#  "parent": "..",
#  "current": ".",
#
#  # vim specific
#  "change this word": "ciw",
#  "beginning of file": "gg",
#  "in the file": "gg",
#  "end of file": "gg",
#  "top of screen": "zt",
#  "center of screen": "zz",
#  "bottom of screen": "zb",
#  "search for this": "*",
#  "scroll up": "",
#  "scroll down": "",
#  "fuzzy search": "",
#  "save": ":w\n",
#  "safe": ":w\n",
#  "file tree": ",t",
#  "file three": ",t",
#  "editor": "vim\n",
#  "edit file": ":e ",
#  "escape": "",
#  "find": "f",
#  "search": "/",
#  "quit": ":q!",
#  "complete": "\t",
#  "internet": "w3m http://www.google.com\n" "zebra":     "z",
