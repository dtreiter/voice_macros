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
  "bruce": "[",
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
  "flower": "*",
  "question": "?",
  "space": " ",
  ",": ",",
  ":": ":",
  ";": ";",
  "period": ".",
  "case": ".",
  "base": ".",
  "ace": ".",
  "quote": "\"",
  "quotes": "\"",
  "\"": "\"",
  "smack": "\"",
  "snack": "\"",
  "mac": "\"",
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
  "escape": "\x1b",
  "undo": "\x1f",
  "tab": "\t",
  "turn": "\t",
  "turned": "\t",
  "enter": "\n",
  "yes": "\r",
  "yeah": "\r",

  # Names as letters
  "albert" : "a",
  "bob" : "b",
  "bill" : "b",
  "carol" : "c",
  "carroll" : "c",
  "caroll" : "c",
  "cici": "cc",
  "daniel" : "d",
  "dede": "dd",
  "didi": "dd",
  "edward" : "e",
  "frederick" : "f",
  "gary" : "g",
  "garry" : "g",
  "gerry" : "g",
  "gigi": "gg",
  "gege": "gg",
  "gargantuan": "G",
  "howard" : "h",
  "high": "i",
  "hi": "i",
  "eye": "i",
  "ireland" : "I",
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
  "yankee": "y",
  "huewai": "yy",
  "wife": "y",
  "zebra" : "z",
  "sibra" : "z",
  "zipper": "z",

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
  "talk": "\x1b[A",
  "down": "\x1b[B",
  "right": "\x1b[C",
  "wright": "\x1b[C",
  "write": "\x1b[C",
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
  "visible": "V",
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

  # useful shortcuts
  "edit": "vim ",
  "internet": "w3m google.com\njjjjjj\t\n",
  "emacs": "emacs"
}

emacs_grammar = {
  # Emacs
  "okay": "fd",
  "switch": " bb",
  "lip": " ww",
  "flip": " ww",
  "helm": " :",
  "compile": " cC\n",
  "home": " :"
}

general_grammar = {
  "trace": "()\x1b[D",
  "string": "\"\"\x1b[D",
  "compare": " == ",
  "equals": " = ",
  "plus": " + ",
  "increment": " += ",
  "increments": " += ",
  "clap": ":",
  "clapp": ":",
  "minus": " - "
}

vacs_grammar = {
  "mode": "mode",
  "fax": "vacs",
  "backs": "vacs",
  "functions": "functions",
  "grammar": "grammar",
  "compiler": "compiler",
  "config": "config",
  "interpreter": "interpreter",
  "token": "token",
  "directory": "directory"
}

python_grammar = {
  "python": "python ",
  "self": "self",
  "return": "return ",
  "finish": "\",\n",
  "from": "from ",
  "import": "import ",
  "hippie": hippie_expand,
  "function": "f" + hippie_expand,
  "value": "d\"" + hippie_expand,
  "loop": "frn" + hippie_expand,

  "lexor": "lexer"
}

c_grammar = {
  "integer": "int",
  "character": "char",
  "condition": "if" + hippie_expand,
  "function": "fun" + hippie_expand,
  "arrow": "->",
  "nothing": "null",
  "structure": "struct",
  "void": "void"
}

shell_grammar = {
  "slap": "\x01\x1b[A",
  "slurp": "\x01\x1b[B",
  "get": "git ",
  "commit": "commit ",
  "addition": "add ",
  "message": "-m ''\x1b[D",
  "status": "status"
}

# A mode is a collection of grammars which is added to the global grammar.
def python_mode():
  WORD_MACROS.update(general_grammar)
  WORD_MACROS.update(emacs_grammar)
  WORD_MACROS.update(python_grammar)
  WORD_MACROS.update(vacs_grammar)

def c_mode():
  WORD_MACROS.update(general_grammar)
  WORD_MACROS.update(emacs_grammar)
  WORD_MACROS.update(python_grammar)
  WORD_MACROS.update(c_grammar)

def shell_mode():
  WORD_MACROS.update(general_grammar)
  WORD_MACROS.update(emacs_grammar)
  WORD_MACROS.update(shell_grammar)

python_mode()
#c_mode()
shell_mode()

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

def capital_case(text):
  output = ''.join(letter for letter in text.title() if letter.isalpha())
  return output

def double_quote(text):
  output = "\"" + text + "\""
  return output

def single_quote(text):
  output = "'" + text + "'"
  return output

def period_case(text):
    output = ".".join(text.lower().split(" "))
    return output

def python_magic(text):
    return "__" + text.lower() + "__"

MACRO_FUNCTIONS = {
  "lower": (lambda text: text.lower()),
  "blower": (lambda text: text.lower()),
  "upper": (lambda text: text.upper()),
  "trim": (lambda text: text.strip()),
  "capital": capital_case,
  "camel": camel,
  "magical": python_magic,
  "hyphenate": hyphen,
  "underline": underscore,
  "dots": period_case,
  "underlined": underscore,
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
