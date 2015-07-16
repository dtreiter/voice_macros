hippie_expand = "\x1a\x1b/\x1a"

WORD_MACROS = {
  # Symbols
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
  "space": " ",
  ",": ",",
  ":": ":",
  ";": ";",
  "quote": "\"",
  "quotes": "\"",
  "\"": "\"",
  "smudge": "'",
  "/": "/",
  "search": "/",
  "peanut": "\\",
  "\\": "\\",

  # Control characters
  "multiplex": "\x01",
  "trash": "\x03",
  "quit": "\x07",
  "backspace": "\x08",
  "complete": "\x0e",
  "insert": "\x12",
  "window": "\x17",
  "extend": "\x18",
  "okay": "\x1b",
  "tab": "\t",
  "turn": "\t",
  "enter": "\n",
  "yes": "\r",

  # Names as letters
  "albert" : "a",
  "bob" : "b",
  "carol" : "c",
  "caroll" : "c",
  "daniel" : "d",
  "edward" : "e",
  "frederick" : "f",
  "gary" : "g",
  "garry" : "g",
  "howard" : "h",
  "ireland" : "i",
  "jeffrey" : "j",
  "christine" : "k",
  "larry" : "l",
  "mark" : "m",
  "nancy" : "n",
  "oscar" : "o",
  "patrick" : "p",
  "quick" : "q",
  "robert" : "r",
  "sarah" : "s",
  "thomas" : "t",
  "ultimate" : "u",
  "umbrella": "U",
  "valerie" : "v",
  "william" : "w",
  "javier" : "x",
  "text" : "x",
  "yolanda" : "y",
  "zebra" : "z",

  # alphabet corrections
  "hey": "a",
  "be": "b",
  "bee": "b",
  "see": "c",
  "egg": "e",
  "eat": "e",
  "find": "f",
  "fine": "f",
  "joe": "j",
  "top": "\x1b[A",
  "down": "\x1b[B",
  "right": "\x1b[C",
  "left": "\x1b[D",
  "mark": "m",
  "in": "n",
  "oh": "o",
  "paste": "p",
  "pope": "p",
  "are": "r",
  "you": "u",
  "the": "v",
  "visual": "V",
  "why": "y",

  # numbers
  "zero": "0",
  "one": "1",
  "two": "2",
  "to": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",

  # Python mode
  "compare": " == ",
  "equals": " = ",
  "plus": " + ",
  "minus": " - ",
  "self": "self",
  "this": "this",
  "return": "return",
  "finish": "\",\n",
  "hippie": hippie_expand,
  "function": "f" + hippie_expand,
  "value": "d\"" + hippie_expand,

  # useful shortcuts
  "edit": "vim ",
  "internet": "w3m google.com\njjjjjj\t\n",
  "emacs": "emacs-24.3 "
}

LETTER_MACROS = {
  # alphabet
  "a": "a",
  "b": "b",
  "c": "c",
  "d": "d",
  "e": "e",
  "f": "f",
  "g": "g",
  "h": "h",
  "i": "i",
  "k": "k",
  "l": "l",
  "m": "m",
  "n": "n",
  "o": "o",
  "p": "p",
  "q": "q",
  "r": "r",
  "s": "s",
  "t": "t",
  "u": "u",
  "v": "v",
  "w": "w",
  "x": "x",
  "y": "y",
  "z": "z"
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
  "blower": (lambda text: text.lower()),
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
