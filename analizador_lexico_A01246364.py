# -----------------------------------------------------------------------------
# analizador_lexico_A01246364.py
#
# Codigo que nos permite ejecutar
# La revisión de sintaxis de nuestro lenguaje de programación	
# Utilizando los modulos ply.lex y ply.yacc
#
# El archivo de entrada representa nuestro programa prueba
# -----------------------------------------------------------------------------
import ply.lex as lex
#import ply.yacc as yacc
program_file = "Programa3_VS.txt"
Program = open(program_file,'r') 

reserved = [
    'INT', 'FLT','STRING','MAIN',
    'IF', 'WHILE','ENDWHILE', 
    'FOR','ENDIF', 'TO',
    'THEN', 'ENDFOR','WRITE', 'READ','ELSE',
    'ROOT',                                                 # Raiz cuadrada

]
tokens = [
    'ID',                                                   # Identificadores 
    'INTV', 'FLTV', 'STRINGV',                              # Tipos de datos
    'PLUS', 'MINUS', 'DIVIDE', 'TIMES',                     # Operadores
    'LPAR', 'RPAR', 'LCAS', 'RCAS', 'LBRK', 'RBRK',         # Parentesis
    'SEMICOLON', 'DOUBLEPOINT', 'COMA',                     # Puntuaciones
    'GT', 'LT', 'GTEQ', 'LTEQ', 'EQUAL', 'NOT','NOTEQ',     # Comparaciones
    'AND', 'OR',                                            # Logicos  
    'ASSIGN',                                               # Asignacion
    'POWER',                                                # Potencia
] 
tokens = tokens + reserved

# Tokens list:
t_EQUAL =  r'\=\='
t_ASSIGN =  r'\='
t_GT =  r'\>'
t_LT =  r'\<'
t_GTEQ =  r'\>\='
t_LTEQ =  r'\<\='
t_NOTEQ =  r'\!\='
t_AND =  r'\&'
t_OR =  r'\|'
t_NOT =  r'\!'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_TIMES = r'\*'
t_POWER = r'\^'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LCAS = r'\['
t_RCAS = r'\]'
t_LBRK = r'\{'
t_RBRK = r'\}'
t_DOUBLEPOINT = r'\:'
t_SEMICOLON = r'\;'
#t_FACTORIAL = r'\!'

#t_COMA = r'\,'
# Ignored characters
t_ignore = ' \t'
# Tipos de datos
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.upper() in tokens: # Verificamos si no esta en el grupo Reservado
        t.value = t.value.upper()
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t    # Return token object

def t_ROOT(t):
    r'ROOT'
    t.type = 'ROOT'
    return t


def t_STRING(t):
    r'STRING'
    t.type = 'STRING'
    return t

def t_INT(t):
    r'INT'
    t.type = 'INT'
    return t

def t_FLT(t):
    r'FLT'
    t.type = 'FLT'
    return t

def t_FLTV(t):
    r'\d*\.\d+' 
    t.value = float(t.value)
    return t

def t_STRINGV(t):
     r'"([^"\n]|(\\"))*"'
     return t

def t_INTV(t):
    r'\d+'
    t.value = int(t.value)
    return t 

#def t_DO(t):
#    r'DO'
#    t.type = 'DO'
#    return t

def t_TO(t):
    r'TO'
    t.type = 'TO'
    return t

def t_ENDIF(t):
    r'ENDIF'
    t.type = 'ENDIF'
    return t

def t_ENDWHILE(t):
    r'ENDWHILE'
    t.type = 'ENDWHILE'
    return t

def t_THEN(t):
    r'THEN'
    t.type = 'THEN'
    return t

def t_ENDFOR(t):
    r'ENDFOR'
    t.type = 'ENDFOR'
    return t
# Funciones
def t_IF(t):
    r'IF'
    t.type = 'IF'
    return t 

def t_ELSE(t):
    r'ELSE'
    t.type = 'ELSE'
    return t

def t_WHILE(t):
    r'WHILE'
    t.type = 'WHILE'
    return t 

def t_FOR(t):
    r'FOR'
    t.type = 'FOR'
    return t 

def t_WRITE(t):
    r'WRITE'
    t.type = 'WRITE'
    return t

def t_READ(t):
    r'READ'
    t.type = 'READ'
    return t

def t_MAIN(t):
    r'MAIN'
    t.type = 'MAIN'
    return t
    
# Extra Functions
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_COMMENT(t):
	r'\#.*'
	pass    # Token discarded

def t_error(t):
    print("Illegal character detected")
    # print("This is the illegal character - > ", tok)
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()
#lexer.input(Program.read())
#while True:
#    tok = lexer.token()
#    print(tok)
#    if not tok: 
#        break
#Program.close()
#print(tok)
