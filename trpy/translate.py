"""

trpy is a small little language that transpiles into python,
mostly for kids that dont know english can dive into programming

"""

import collections
import re
import sys
from collections import OrderedDict
import functools
registered_tokens = OrderedDict()

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

def tokenize(s):
    token_specification = []

    for tok in registered_tokens.values():
        token_specification.append( tok[0:-1] )

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line = 1
    pos = line_start = 0
    mo = get_token(s)
    while mo is not None:
        typ = mo.lastgroup
        if typ == 'NEWLINE':
            line_start = pos
            line += 1
            yield Token(typ, mo.group(typ), line, mo.start()-line_start)
        else:
            val = mo.group(typ)
            yield Token(typ, val, line, mo.start()-line_start)
        pos = mo.end()
        mo = get_token(s, pos)
    if pos != len(s):
        raise RuntimeError('Unexpected character %r on line %d' %(s[pos], line))

def token(token_name, regexp):
    def wrap_f(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        registered_tokens[token_name] = (token_name, regexp, inner)
        return inner
    return wrap_f

@token('FUNC', r'(.*?)->')
def t_FUNC(token_value, state):
    indent = ""
    tv = token_value
    indents = re.match('(^[\ ]+?)[a-zA-Z0-9_]', token_value)
    if indents:
        indent = indents.groups()[0]
        tv = re.sub(r'^[\ ]+', '', token_value)
    func_def = ' '.join(tv.split('->')[:-1])
    if '(' not in func_def:
        func_def = "%s()" % func_def
    l = "%sdef %s:" % (indent, func_def)
    return (l, state)

@token('OR', r'veya')
def t_OR(token_value, state):
    return 'or', state

@token('AND', r've')
def t_AND(token_value, state):
    return 'and', state

@token('IMPORT', r'yukle, (.*)')
def t_IMPORT(token_value, state):
    t = re.match('yukle,(.*?) icinden (.*)', token_value)
    if t:
        return 'from %s import %s' % (t.groups()[0], t.groups()[1]), state
    else:
        t = re.match('yukle,(.*)', token_value)
        return 'import %s' % t.groups()[0], state

@token('IF', r'eger,(.*)')
def t_IF(token_value, state):
    t = re.match('eger,(.*?) ise', token_value)
    s = t.groups()[0]
    tokens = list(tokenize(s))
    code = translate(tokens)
    return 'if%s:'% code, state

@token('WHILE', r'durum,(.*)')
def t_WHILE(token_value, state):
    t = re.match('durum,(.*?) iken', token_value)
    s = t.groups()[0]
    tokens = list(tokenize(s))
    code = translate(tokens)
    return 'while%s:'% code, state

@token('FOR', r'her bir,(.*)')
def t_FOR(token_value, state):
    t = re.match('her bir,(.*?) icin (.*)', token_value)
    variable = t.groups()[0]
    iterable = t.groups()[1]
    return 'for %s in %s:'% (iterable, variable), state

@token('ELIF', r'ya da,(.*)')
def t_ELIF(token_value, state):
    t = re.match('ya da,(.*)', token_value)
    s = t.groups()[0]
    tokens = list(tokenize(s))
    code = translate(tokens)
    if code == "":
        l = "else:"
    else:
        l = 'elif%s:'% code
    return l, state

@token('RETURN', r'<-')
def t_RETURN(token_value, state):
    return ('return', state)

@token('PRINT', r'yazdir (.*?)')
def t_PRINT(token_value, state):
    return ('print ', state)

@token('OTHER', r'.')
def t_OTHER(token_value, state):
    return (token_value, state)

@token('WS', r' ')
def t_WS(token_value, state):
    return (token_value, state)

@token('NEWLINE', r'\n')
def t_NEWLINE(token_value, state):
    return (token_value, state)

def translate_token(token, state=None):
    if token.typ == 'NEWLINE':
        if state == None:
            return (token.value, "NEWLINE")
        else:
            return (token.value, state)

    fn = registered_tokens[token.typ][-1]
    return fn(token.value, state)

def translate(tokens):
    buf = ''
    state = None
    for token in tokens:
        t, state = translate_token(token, state)
        buf += t
    return buf

def transpile(filename):
    f = open(sys.argv[1], 'r')
    tokens = list(tokenize(f.read()))
    code = translate(tokens)

import os
import imp
import __future__

class TrpySyntaxError(Exception):
    pass

def translate_file(filename=None):
    if not filename:
        filename = sys.argv[1]
    f = open(filename, 'r')
    tokens = list(tokenize(f.read()))
    code = translate(tokens)
    print code

def compile_file(filename, module_name=None):
    f = open(filename, 'r')
    tokens = list(tokenize(f.read()))
    code = translate(tokens)
    ast = compile(code, filename, "exec")
    return ast

def run_file(filename=None):
    if not filename:
        filename = sys.argv[1]
    try:
        import_file_to_module("__main__", filename)
    except Exception:
        raise

# def run_file():
#     print ">>>>"
#     s = open('t.trpy').read()
#     tokens = list(tokenize(s))
#     code = translate(tokens)
#     print code
#     ast = compile(code, "<string>", "exec")
#     exec(code)

    # filename = sys.argv[1]
    # try:
    #     ast = compile_file(filename)
    # except Exception as e:
    #     exc = TrpySyntaxError(e)
    #     raise exc
    # exec(ast)

def ast_compile(ast, filename, mode):
    """Compile AST.
    Like Python's compile, but with some special flags."""
    flags = (__future__.CO_FUTURE_DIVISION |
             __future__.CO_FUTURE_PRINT_FUNCTION)
    return compile(ast, filename, mode, flags)

def import_file_to_module(module_name, fpath):
    """Import content from fpath and puts it into a Python module.

    Returns the module."""
    try:
        _ast = compile_file(fpath, module_name)
        mod = imp.new_module(module_name)
        mod.__file__ = fpath
        eval(_ast, mod.__dict__)
    except TrpySyntaxError as e:
        if e.source is None:
            with open(fpath, 'rt') as fp:
                e.source = fp.read()
            e.filename = fpath
        raise
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return mod

class MetaLoader(object):
    def __init__(self, path):
        self.path = path

    def is_package(self, fullname):
        dirpath = "/".join(fullname.split("."))
        for pth in sys.path:
            pth = os.path.abspath(pth)
            composed_path = "%s/%s/__init__.trpy" % (pth, dirpath)
            if os.path.exists(composed_path):
                return True
        return False

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        if not self.path:
            return

        sys.modules[fullname] = None
        mod = import_file_to_module(fullname,
                                    self.path)

        ispkg = self.is_package(fullname)

        mod.__file__ = self.path
        mod.__loader__ = self
        mod.__name__ = fullname

        if ispkg:
            mod.__path__ = []
            mod.__package__ = fullname
        else:
            mod.__package__ = fullname.rpartition('.')[0]

        sys.modules[fullname] = mod
        return mod



class MetaImporter(object):

    def find_on_path(self, fullname):
        fls = ["%s/__init__.trpy", "%s.trpy"]
        dirpath = "/".join(fullname.split("."))
        for pth in sys.path:
            pth = os.path.abspath(pth)
            for fp in fls:
                composed_path = fp % ("%s/%s" % (pth, dirpath))
                if os.path.exists(composed_path):
                    return composed_path

    def find_module(self, fullname, path=None):
        path = self.find_on_path(fullname)
        if path:
            return MetaLoader(path)


sys.meta_path.append(MetaImporter())
sys.path.insert(0, "")




if __name__ == "__main__":
    f = open(sys.argv[1], 'r')
    tokens = list(tokenize(f.read()))
    code = translate(tokens)
    print code
