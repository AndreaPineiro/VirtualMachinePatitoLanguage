# ------------------------------------------------------------
# PatitoLexer.py
#
# Tokenizer for elements in Patito language
# ------------------------------------------------------------

import ply.lex as lex

class PatitoLexer(object):

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self,**kwargs)

    # List of reserved words
    reserved = {
        'program': 'PROGRAM',
        'end': 'END',
        'var': 'VAR',
        'cout': 'COUT',
        'if' : 'IF',
        'else': 'ELSE',
        'elif': 'ELIF',
        'int': 'INT',
        'float': 'FLOAT',
        'do': 'DO',
        'while': 'WHILE'
    }

    # List of token names
    tokens = [
        'CTE_INT',
        'CTE_FLOAT',
        'CTE_STRING',
        'ID',
        'LEFT_PARENTHESIS',
        'RIGHT_PARENTHESIS',
        'LEFT_BRACE',
        'RIGHT_BRACE',
        'COLON',
        'COMMA',
        'SEMICOLON',
        'EQUAL',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'GREATER_THAN',
        'LESS_THAN',
        'DIFFERENT_THAN',
    ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_LEFT_PARENTHESIS = r'\('
    t_RIGHT_PARENTHESIS = r'\)'
    t_LEFT_BRACE = r'\{'
    t_RIGHT_BRACE = r'\}'
    t_COLON = r'\:'
    t_COMMA = r'\,'
    t_SEMICOLON = r'\;'
    t_EQUAL = r'\='
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_GREATER_THAN = r'\>'
    t_LESS_THAN = r'\<'
    t_DIFFERENT_THAN = r'\!='

    # Definition of rules
    def t_CTE_STRING(self, t):
        r'[\"|\'].*?[\"|\']'
        t.value = t.value[1:-1] # Elimina las comillas
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    def t_CTE_FLOAT(self, t):
        r'[0-9]+\.[0-9]+'
        t.value = float(t.value)
        return t

    def t_CTE_INT(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    # Track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Non valid character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Test lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Build and test lexer
if __name__ == '__main__':
    data = '''
    123 x 48.234
    "hola" _count
    program end var cout if else int float do while
    'andrea'
    ( ) { } : ; , =
    + - * / > < !=
    $
    '''
    m = PatitoLexer()
    m.build()
    m.test(data)