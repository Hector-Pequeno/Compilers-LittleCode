import analizador_lexico_A01246364 as myLexer
import ply.yacc as yacc

tokens = myLexer.tokens
#Resolver NOT

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
    program : MAIN LPAR RPAR LBRK estatutos RBRK
    '''
                                                          # main(){ estatutos }
def p_estatutos(p):
    '''
    estatutos : dec_Var estatutos
              | act_Var estatutos
              | dec_Arr estatutos
              | act_Arr estatutos
              | f_write estatutos
              | f_read  estatutos
              | e_if    estatutos
              | e_while estatutos
              | e_for   estatutos
              | empty
              
    '''
                                                          # Declaracion de variables /
                                                          # Actualizacion de variables /
                                                          # Declaracion de variables tipo arreglo /
                                                          # Actualizacion de variables tipo arreglo /
                                                          # Funciones predefinida  - Write (Equivalente al Print) /
                                                          # Funciones predefinida  - Read /
                                                          # Estatuto IF /
                                                          # Estatuto WHILE / 
                                                          # Estatuto FOR
                                                          # Posibilidad de Crear funciones               | c_func  estatutos
                                                          # El programa MAIN puede estar vacio (definicion empty) /
#   DECLARACION ESTATUTOS   IF    #
def p_estatuto_if(p):
    '''
    e_if : IF LPAR comp_expression RPAR THEN estatutos ENDIF
         | IF LPAR comp_expression RPAR THEN estatutos ELSEIF LPAR comp_expression RPAR THEN estatutos ENDIF
         
    '''

#   DECLARACION ESTATUTOS   WHILE    #
def p_estatuto_while(p):
    '''
    e_while : DO estatutos WHILE LPAR comp_expression RPAR ENDWHILE
    '''

#   DECLARACION ESTATUTOS   FOR    #
def p_estatuto_for(p):
    '''
    e_for : FOR LPAR dec_Var comp_expression SEMICOLON incdec RPAR THEN estatutos ENDFOR
    '''

#   ESTRUCTURA DE INCREMENTO Y DECREMENTO
def p_incdec(p):
    '''
    incdec : ID INC
           | ID DEC
    '''

#def p_estatuto_elseif(p):
#    '''
#    e_elseif : ELSEIF LPAR expression RPAR THEN estatutos e_elseif
#    '''

#   DECLARACION DE VARIABLES    #
def p_dec_Var(p):
    '''
    dec_Var : ID DOUBLEPOINT type ASSIGN expression SEMICOLON
            | ID DOUBLEPOINT type SEMICOLON
    '''
                                                          # NOMBRE_VAR : INT/STRING/FLOAT  = V_int/V_string/V_float/variable ;
                                                          # NOMBRE_VAR : INT/FLOAT/STRING ;
                                                          # igualar a una expresion
#   ACTUALIZACION DE VARIABLES  #
def p_act_Var(p):
    '''
    act_Var : ID ASSIGN expression SEMICOLON
    '''
                                                          # NOMBRE_VAR = V_int/V_string/V_float/variable ;

#   DECLARACION DE VARIABLES TIPO ARREGLO     #
def p_dec_Arr(p):
    '''
    dec_Arr : ID dimension DOUBLEPOINT type SEMICOLON
    '''
                                                          # NOMBRE_VAR DIMENSION : INT/FLOAT/STRING ; Aun no se inicializan con un valor

#   ACTUALIZACION DE VARIABLES TIPO ARREGLO     #
def p_act_Arr(p):
    '''
    act_Arr : ID dimension ASSIGN expression SEMICOLON
    '''
                                                          # NOMBRE_VAR DIMENSION = V_int/V_string/V_float/variable ;

#   DECLARACION - DIMENSIONES POSIBLES Y SU COTENIDO
def p_dimension(p):
    '''
    dimension : LCAS expression RCAS
              | LCAS expression RCAS LCAS expression RCAS
              | LCAS expression RCAS LCAS expression RCAS LCAS expression RCAS
    '''
                                                          # Dimensiones con indices, tanto de tipo entero o variables
                                                          # ARR[V_int/ID], ARR[V_int/ID][V_int/ID], ARR[V_int/ID][V_int/ID][V_int/ID]

#   TIPOS DE DATOS    #
def p_type(p):
    '''
    type : INT
         | FLT
         | STRING
    '''
                                                          # Tipos de datos -> INT, FLT, STRING 

#   TIPOS DE VALORES ASIGNABLES   #
#Modificar
#def p_value(p):
#    '''
#    value : INTV
#          | FLTV
#          | STRINGV
#          | expression
#          | ID
#    '''
                                                          # Tipos de datos asignables -> INT, FLT, STRING y variables

#   FUNCION WRITE (PRINT)   #
def p_write(p):
    '''
    f_write : WRITE LPAR expression RPAR SEMICOLON
    '''
                                                          # WRITE(ID/V_string/V_int,V_float)

#   FUNCION READ   #
def p_read(p):
    '''
    f_read : READ LPAR expression RPAR SEMICOLON
    '''
                                                          # READ(ID/V_string/V_int,V_float)

#   Expresiones ARITMETICAS   #
def p_aritmetic_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | constante
    '''

#   Expresiones COMPARATIVAS   #
def p_comp_expression(p):
    '''
    comp_expression : expression EQUAL expression
                    | expression GT expression
                    | expression LT expression
                    | expression GTEQ expression
                    | expression LTEQ expression
                    | expression NOTEQ expression
                    | expression AND expression
                    | expression OR expression
                    | expression NOT expression
    '''
#   Expresiones LOGICAS         #
#def p_logicas(p):
#    '''
#    logicas : AND
#            | OR
#            | NOT
#    '''

#   CONSTANTES NUMERICAS para ser utilizadas en las expresiones
def p_constante_num(p):
    '''
    constante : INTV
              | FLTV
    '''

#   CONSTANTES DE ID para ser utilizadas en las expresiones, como variables y arreglos
def p_constante_ID(p):
    '''
    constante : ID
              | ID dimension
    '''

#   DEFINICION DE EMPTY     #
def p_empty(p):
    'empty :'
    pass
                                                          # Revisa un conjunto vacio

#   DEFINICION DE ERROR     #
def p_error(p):
    print("Syntax error found")
    print(p)
                                                          # Indica donde se ecuentra un error de sintaxis
parser = yacc.yacc()
try:
    with open("Programa_Prueba.txt",  encoding="utf8") as f:
        file = f.read()
    parser.parse(file)
except EOFError:
    pass
print("Fin de lectura")