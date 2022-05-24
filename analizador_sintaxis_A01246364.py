import analizador_lexico_A01246364 as myLexer
#import math
import ply.yacc as yacc

debug = True
tokens = myLexer.tokens + myLexer.reserved
#errorCounter = 0


# To resolve ambiguity, especially in expression grammars,
# yacc.py allows individual tokens to be assigned a precedence 
# level and associativity. This is done by adding a variable 
# precedence to the grammar
# Order: Lower Precedence to Higher Precedence
# left -> Associativiy
# Same level, same precedence
precedence = (
    ('nonassoc', 'GT', 'LT', 'GTEQ', 'LTEQ'), # Nonassociative operators - comparison operators like < and > but you didn't want to allow combinations like a < b < c 
    ('left','AND','OR'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    #('right', 'UMINUS'),            # Unary minus operator
)

def p_program(p):
    '''
    program : MAIN LPAR RPAR LBRK body RBRK
    '''
#   Programa -> main(){ Variables + Funciones + Estatutos }
###   Body Incuye Variables, Funciones y Estatutos

def p_body(p):
    '''
    body    : body variable
            | body estatutos
            | body expresionAritmeticaID SEMICOLON
            | body ID ASSIGN asignacion SEMICOLON
            | body ID LCAS INTV RCAS ASSIGN asignacion SEMICOLON
            | body ID LCAS INTV RCAS LCAS INTV RCAS ASSIGN asignacion SEMICOLON
            | body ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS ASSIGN asignacion SEMICOLON
            | body ID LCAS ID RCAS ASSIGN asignacion SEMICOLON
            | body ID LCAS ID RCAS LCAS ID RCAS ASSIGN asignacion SEMICOLON
            | body ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS ASSIGN asignacion SEMICOLON
            | empty
    '''
#   Nos dirige a como se define una variable
#   Nos dirige a como se definen las funciones
#   Nos dirife a como se definen los estatutos (FOR, WHILE, IF)
#   Puede ser una programa vacio
###   El body que se antepone indica que se pueden definir mas variables, funciones y estatutos

def p_variable(p):
    '''
    variable : ID DOUBLEPOINT INT ASSIGN INTV SEMICOLON
             | ID DOUBLEPOINT FLT ASSIGN FLTV SEMICOLON
             | ID DOUBLEPOINT STRING ASSIGN STRINGV SEMICOLON
             | ID LCAS INTV RCAS DOUBLEPOINT type SEMICOLON
             | ID LCAS INTV RCAS LCAS INTV RCAS DOUBLEPOINT type SEMICOLON
             | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS DOUBLEPOINT type SEMICOLON
    '''
#   Declaracion de variables tipo INT       -> ID : tipoINT     = Valor ;
#   Declaracion de variables tipo FLT       -> ID : tipoFLT     = Valor ;
#   Declaracion de variables tipo STRING    -> ID : tipoSTRING  = "Valor" ;
#   Declaracion de variables tipo Matriz 1D -> ID[valor_int] : tipo = Valor;
#   Declaracion de variables tipo Matriz 2D -> ID[valor_int][valor_int] : tipo = Valor;
#   Declaracion de variables tipo Matriz 3D -> ID[valor_int][valor_int][valor_int] : tipo = Valor;

def p_variableFor(p):
    '''
    variableFor : ID DOUBLEPOINT INT ASSIGN INTV
    '''
#   Declaracion de variables tipo INT       -> ID : tipoINT     = Valor ;

def p_estatutos(p):
    '''
    estatutos : fFor
              | fWhile
              | fIf
    '''
#   Nos redirige a la funcion de un ciclo FOR
#   Nos redirige a la funcion de un ciclo WHILE
#   Nos redirige a la funcion de un ciclo IF
#   Nos redirige a la funcion de asignacion
def p_asignacion(p):
    '''
    asignacion : variablesInicializadas 
               | variablesInicializadas PLUS variablesInicializadas 
               | variablesInicializadas MINUS variablesInicializadas 
               | variablesInicializadas TIMES variablesInicializadas 
               | variablesInicializadas DIVIDE variablesInicializadas 
               | variablesInicializadas POWER variablesInicializadas 
    '''

def p_variablesInicializadas(p):
    '''
    variablesInicializadas : ID
             | ID LCAS INTV RCAS
             | ID LCAS INTV RCAS LCAS INTV RCAS
             | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
             | ID LCAS ID RCAS
             | ID LCAS ID RCAS LCAS ID RCAS
             | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
    '''
def p_fIf(p):
    '''
    fIf : IF LPAR expresionLogica RPAR THEN body ENDIF
        | IF LPAR expresionLogica RPAR THEN body else ENDIF
    '''
#   IF (x < 3) THEN cuerpo ENDIF
#   IF (x < 3) THEN cuerpo ELSEif cuerpo ENDIF

def p_else(p):
    '''
    else : ELSEIF LPAR expresionLogica RPAR THEN 
    '''


def p_expresionLogica(p):
    '''
    expresionLogica    : ID GTEQ ID
                       | ID LTEQ ID
                       | ID GT ID
                       | ID LT ID
                       | INTV GTEQ INTV
                       | INTV LTEQ INTV
                       | INTV GT INTV
                       | INTV LT INTV
                       | INTV GTEQ ID
                       | INTV LTEQ ID
                       | INTV GT ID
                       | INTV LT ID
                       | ID GTEQ INTV
                       | ID LTEQ INTV
                       | ID GT INTV
                       | ID LT INTV
                       | expresionAritmetica GTEQ INTV
                       | expresionAritmetica LTEQ INTV
                       | expresionAritmetica GT INTV
                       | expresionAritmetica LT INTV
                       | INTV GTEQ expresionAritmetica
                       | INTV LTEQ expresionAritmetica
                       | INTV GT expresionAritmetica
                       | INTV LT expresionAritmetica
                       | expresionAritmetica GTEQ ID
                       | expresionAritmetica LTEQ ID
                       | expresionAritmetica GT ID
                       | expresionAritmetica LT ID
                       | ID GTEQ expresionAritmetica
                       | ID LTEQ expresionAritmetica
                       | ID GT expresionAritmetica
                       | ID LT expresionAritmetica
                       | expresionAritmetica GTEQ expresionAritmetica
                       | expresionAritmetica LTEQ expresionAritmetica
                       | expresionAritmetica GT expresionAritmetica
                       | expresionAritmetica LT expresionAritmetica
                       | ID EQUAL ID
                       | INTV EQUAL INTV
                       | INTV EQUAL ID
                       | ID EQUAL INTV
                       | expresionAritmetica EQUAL INTV
                       | INTV EQUAL expresionAritmetica
                       | expresionAritmetica EQUAL ID
                       | ID EQUAL expresionAritmetica
                       | expresionAritmetica EQUAL expresionAritmetica
                       | ID NOT ID
                       | INTV NOT INTV
                       | INTV NOT ID
                       | ID NOT INTV
                       | expresionAritmetica NOT INTV
                       | INTV NOT expresionAritmetica
                       | expresionAritmetica NOT ID
                       | ID NOT expresionAritmetica
                       | expresionAritmetica NOT expresionAritmetica
    '''

def p_expresionLogicaFORWHILE(p):
    '''
    expresionLogicaFORWHILE : ID GTEQ ID
                       | ID LTEQ ID
                       | ID GT ID
                       | ID LT ID
                       | INTV GTEQ INTV
                       | INTV LTEQ INTV
                       | INTV GT INTV
                       | INTV LT INTV
                       | INTV GTEQ ID
                       | INTV LTEQ ID
                       | INTV GT ID
                       | INTV LT ID
                       | ID GTEQ INTV
                       | ID LTEQ INTV
                       | ID GT INTV
                       | ID LT INTV
                       | expresionAritmetica GTEQ INTV
                       | expresionAritmetica LTEQ INTV
                       | expresionAritmetica GT INTV
                       | expresionAritmetica LT INTV
                       | INTV GTEQ expresionAritmetica
                       | INTV LTEQ expresionAritmetica
                       | INTV GT expresionAritmetica
                       | INTV LT expresionAritmetica
                       | expresionAritmetica GTEQ ID
                       | expresionAritmetica LTEQ ID
                       | expresionAritmetica GT ID
                       | expresionAritmetica LT ID
                       | ID GTEQ expresionAritmetica
                       | ID LTEQ expresionAritmetica
                       | ID GT expresionAritmetica
                       | ID LT expresionAritmetica
                       | expresionAritmetica GTEQ expresionAritmetica
                       | expresionAritmetica LTEQ expresionAritmetica
                       | expresionAritmetica GT expresionAritmetica
                       | expresionAritmetica LT expresionAritmetica
    '''
#   x >= y
#   x <= y
#   x > y
#   x < y
#   10 >= 5
#   10 <= 5
#   10 > 5
#   10 < 5
#   10 >= x
#   10 <= x
#   10 > x
#   10 < x
#   x >= 5
#   x <= 5
#   x > 5
#   x < 5


def p_fWhile(p):
    '''
    fWhile : DO THEN body WHILE LPAR expresionLogicaFORWHILE RPAR ENDWHILE
    '''
#   Declaracion -> DO THEN cuerpo WHILE ( x < 10 )ENDWHILE    

def p_fFor(p):
    '''
    fFor    : FOR LPAR variableFor SEMICOLON expresionLogicaFORWHILE SEMICOLON expresionAritmeticaID RPAR THEN body ENDFOR
    '''
#   Declaracion -> FOR (x : int = 0 ; x < 10 ; x++){ cuerpo }

def p_expresionAritmetica(p):
    '''
    expresionAritmetica : suma
                        | resta
    '''

def p_division(p):
    '''
    division : INTV DIVIDE INTV
             | ID INTV DIVIDE INTV
             | INTV DIVIDE ID
             | ID DIVIDE ID
             | ID LCAS INTV RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS INTV RCAS
             | ID LCAS INTV RCAS DIVIDE ID LCAS INTV RCAS
             | ID LCAS INTV RCAS LCAS INTV RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS INTV RCAS LCAS INTV RCAS
             | ID LCAS INTV RCAS LCAS INTV RCAS DIVIDE ID LCAS INTV RCAS LCAS INTV RCAS     
             | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
             | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS DIVIDE ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
             | ID LCAS ID RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS ID RCAS
             | ID LCAS ID RCAS DIVIDE ID LCAS ID RCAS
             | ID LCAS ID RCAS LCAS ID RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS ID RCAS LCAS ID RCAS
             | ID LCAS ID RCAS LCAS ID RCAS DIVIDE ID LCAS ID RCAS LCAS ID RCAS     
             | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS DIVIDE INTV
             | INTV DIVIDE ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
             | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS DIVIDE ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
    '''


def p_multiplicacion(p):
    '''
    multiplicacion : INTV TIMES INTV
                   | ID INTV TIMES INTV
                   | INTV TIMES ID
                   | ID TIMES ID
                   | ID LCAS INTV RCAS TIMES INTV
                   | INTV TIMES ID LCAS INTV RCAS
                   | ID LCAS INTV RCAS TIMES ID LCAS INTV RCAS
                   | ID LCAS INTV RCAS LCAS INTV RCAS TIMES INTV
                   | INTV TIMES ID LCAS INTV RCAS LCAS INTV RCAS
                   | ID LCAS INTV RCAS LCAS INTV RCAS TIMES ID LCAS INTV RCAS LCAS INTV RCAS     
                   | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS TIMES INTV
                   | INTV TIMES ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
                   | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS TIMES ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
                   | ID LCAS ID RCAS TIMES INTV
                   | INTV TIMES ID LCAS ID RCAS
                   | ID LCAS ID RCAS TIMES ID LCAS ID RCAS
                   | ID LCAS ID RCAS LCAS ID RCAS TIMES INTV
                   | INTV TIMES ID LCAS ID RCAS LCAS ID RCAS
                   | ID LCAS ID RCAS LCAS ID RCAS TIMES ID LCAS ID RCAS LCAS ID RCAS     
                   | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS TIMES INTV
                   | INTV TIMES ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
                   | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS TIMES ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
    '''

def p_expresionAritmeticaID(p):
    '''
    expresionAritmeticaID : suma
                          | resta
                          | multiplicacion
                          | division
                          | incremento
                          | decremento
    '''
#   Dirigimos la rutina a las expresiones aritmeticas de
#   Suma
#   Incremento
#   Resta
#   Decremento

def p_suma(p):
    '''
    suma : INTV PLUS INTV
         | ID INTV PLUS INTV
         | INTV PLUS ID
         | ID PLUS ID
         | ID LCAS INTV RCAS PLUS INTV
         | INTV PLUS ID LCAS INTV RCAS
         | ID LCAS INTV RCAS PLUS ID LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS PLUS INTV
         | INTV PLUS ID LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS PLUS ID LCAS INTV RCAS LCAS INTV RCAS     
         | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS PLUS INTV
         | INTV PLUS ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS PLUS ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS ID RCAS PLUS INTV
         | INTV PLUS ID LCAS ID RCAS
         | ID LCAS ID RCAS PLUS ID LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS PLUS INTV
         | INTV PLUS ID LCAS ID RCAS LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS PLUS ID LCAS ID RCAS LCAS ID RCAS     
         | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS PLUS INTV
         | INTV PLUS ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS PLUS ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
    '''
#   Definicion de la suma, donde se pueden sumar 2 o mas terminos
#   Suma de valor + variables
#   Suma de valores + arreglo de una dimension (dimension constante)
#   Suma de valores + arreglo de dos dimensiones (dimension constante)
#   Suma de valores + arreglo de tres dimensiones (dimension constante)
#   Suma de valores + arreglo de una dimension (dimension ID)
#   Suma de valores + arreglo de dos dimensiones (dimension ID)
#   Suma de valores + arreglo de tres dimensiones (dimension ID)

def p_incremento(p):
    '''
    incremento : ID INC
    '''
#   Definicion del incremento, donde se puede aumentar el valor de una variable

def p_resta(p):
    '''
    resta : INTV MINUS INTV
         | ID INTV MINUS INTV
         | INTV MINUS ID
         | ID MINUS ID
         | ID LCAS INTV RCAS MINUS INTV
         | INTV MINUS ID LCAS INTV RCAS
         | ID LCAS INTV RCAS MINUS ID LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS MINUS INTV
         | INTV MINUS ID LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS MINUS ID LCAS INTV RCAS LCAS INTV RCAS     
         | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS MINUS INTV
         | INTV MINUS ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS MINUS ID LCAS INTV RCAS LCAS INTV RCAS LCAS INTV RCAS
         | ID LCAS ID RCAS MINUS INTV
         | INTV MINUS ID LCAS ID RCAS
         | ID LCAS ID RCAS MINUS ID LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS MINUS INTV
         | INTV MINUS ID LCAS ID RCAS LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS MINUS ID LCAS ID RCAS LCAS ID RCAS     
         | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS MINUS INTV
         | INTV MINUS ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
         | ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS MINUS ID LCAS ID RCAS LCAS ID RCAS LCAS ID RCAS
    '''
    
#   Definicion de la resta, donde se pueden restar 2 o mas terminos
#   Resta de valor + variables
#   Resta de valores + arreglo de una dimension (dimension constante)
#   Resta de valores + arreglo de dos dimensiones (dimension constante)
#   Resta de valores + arreglo de tres dimensiones (dimension constante)
#   Resta de valores + arreglo de una dimension (dimension ID)
#   Resta de valores + arreglo de dos dimensiones (dimension ID)
#   Resta de valores + arreglo de tres dimensiones (dimension ID)

def p_decremento(p):
    '''
    decremento : ID DEC
    '''
#   Definicion del decremento, donde se puede restar el valor de una variable

def p_type(p):
    '''
    type    : STRING
            | INT
            | FLT
    '''

def p_empty(p):
     'empty :'
     pass

def p_error(p):
    print("Syntax error found")
    print(p)

parser = yacc.yacc()
try:
    with open("Programa_correcto2.txt",  encoding="utf8") as f:
        file = f.read()
    parser.parse(file)
except EOFError:
    pass
print("Fin de lectura")