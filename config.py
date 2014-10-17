# simple macros (ie. list -> ls)
MACROS = {
  # typing characters
  "enter": "\n",
  "space": " ",
  "backspace": "",
  ",": ",",
  ":": ":",
  ";": ";",
  "quote": "\"",
  "single quote": "'",
  "/": "/",

  # alphabet
  "a":    "a",
  "hey": "a",
  "be":    "b",
  "c": "c",
  "see":  "c",
  "d":    "d",
  "e":     "e",
  "f":  "f",
  "g":     "g",
  "h":    "h",
  "eight":    "h",
  "i":    "i",
  "joe":   "j",
  "k":     "k",
  "l":     "l",
  "m":     "m",
  "in": "n",
  "o":    "o",
  "p":     "p",
  "q":   "q",
  "are":    "r",
  "s":   "s",
  "t":    "t",
  "you":  "u",
  "the":   "v",
  "w":  "w",
  "x":     "x",
  "why":   "y",
  "zebra":     "z",

  # terminal
  "list": "ls",
  "change": "cd ",
  "print me": "pwd",
  "parent": "..",
  "current": ".",

  # vim specific
  "change this word": "ciw",
  "top of screen": "zt",
  "center of screen": "zz",
  "bottom of screen": "zb",
  "search for this": "*",
  "fuzzy search": "",
  "save": ":w\n",
  "file tree": ",t",
  "editor": "vim\n",
  "edit file": ":e ",
  "escape": "",
  "find": "f",
  "search": "/",
  "quit": ":q!",
  "complete": "\t",
  "internet": ":W3m http://www.google.com\n"
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

MACRO_FUNCTIONS = {
  "lower": (lambda text: text.lower()),
  "upper": (lambda text: text.upper()),
  "capital": (lambda text: text.title()),
  "trim": (lambda text: text.strip()),
  "camel": camel,
  "hyphenate": hyphen,
  "underline": underscore,
  "say": (lambda text: text)
}
