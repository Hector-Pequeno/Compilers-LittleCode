import analizador_lexico_A01246364 as myLexer
import ply.yacc as yacc
import sys as compilador

tokens = myLexer.tokens

#   INICIO TABLA DE SIMBOLOS   #
Simbol_Index = 0       # Posición inicial de la tabla de simbolos
tabla_de_simbolos = {} # Lista vacia, donde seran guardados nuestros simbolos

#   CUADRUPLOS      #

pila_operandos = [] # Arreglo de operandos
temporales = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T22', 'T23', 'T24'] #Lista de temporales

def cuadruplos(operation, operand1, operand2, result):
                # Formato de armado de cuadruplos
    cuadruplo = [operation, operand1, operand2, result] # Armamos el cuadruplo
    print("Cuadruplo -> ",cuadruplo) #Imprimimos el cuadruplo
    print(pila_operandos)

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
    program : program main
            | program dec_func
            | empty
    '''
                                                          # funcion_n(){estatutos}  y|o  main(){ estatutos }  y|o vacio
                                                    
def p_main(p):
    '''
    main : MAIN LPAR RPAR LBRK estatutos RBRK
    '''
                                                          # main(){ estatutos }
def p_estatutos(p):
    '''
    estatutos : estatutos dec_Var 
              | estatutos act_Var 
              | estatutos dec_Arr 
              | estatutos act_Arr 
              | estatutos f_write 
              | estatutos f_read  
              | estatutos e_if    
              | estatutos e_while 
              | estatutos e_for   
              | estatutos c_func  
              | estatutos comp_expression SEMICOLON
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
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} is not declared!")
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result   = simbolo     
    pila_operandos.append(result)
    if(  p[2] == '++'):
        cuadruplos('++',operand1, operand2, result)
    elif(p[2] == '--'):
        cuadruplos('--',operand1, operand2, result)
                                                          # Nos indica como se ejecuta un incremento i++, i--
def p_dec_Var(p):
    '''
    dec_Var : ID DOUBLEPOINT type ASSIGN expression SEMICOLON
            | ID DOUBLEPOINT type SEMICOLON
    '''
                                                          # NOMBRE_VAR : INT/STRING/FLOAT  = V_int/V_string/V_float/variable ;
                                                          # NOMBRE_VAR : INT/FLOAT/STRING ;
                                                          # igualar a una expresion
    #    ACTUALIZACION TABLA DE SIMBOLOS  #
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = p[3]  # Obtenemos el tipo de la variable
    #print("p[1] = ",p[1],"p[2] = ",p[2],"p[3] = ",p[3],"p[4] = ",p[4], "p[5] = ",p[5],"p[6] = ",p[6])
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Already declared!")
    else:
        # Tabla de simbolos
        tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
        tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
        tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
        Simbol_Index = Simbol_Index + 1 # Incrementamos la posicion de la tabla de simbolos
        # Cuadruplos
        operand1 = pila_operandos.pop()
        result   = simbolo     
        pila_operandos.append(result)
        cuadruplos('=',operand1," ", result)
#   ACTUALIZACION DE VARIABLES  #
def p_act_Var(p):
    '''
    act_Var : ID ASSIGN expression SEMICOLON
    '''
                                                          # NOMBRE_VAR = V_int/V_string/V_float/variable ;
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} is not declared!")
    operand1 = pila_operandos.pop()
    result   = simbolo
    if not simbolo in pila_operandos:                     # Si ya existe en memoria, no lo volvemos a declarar. solo en asignacion
        pila_operandos.append(result)
        cuadruplos('=',operand1," ", result)
    else:
        cuadruplos('=',operand1," ", result)

#   DECLARACION DE VARIABLES TIPO ARREGLO     #
def p_dec_Arr(p):
    '''
    dec_Arr : ID dimension DOUBLEPOINT type SEMICOLON
    '''
                                                          # NOMBRE_VAR DIMENSION : INT/FLOAT/STRING ; Aun no se inicializan con un valor
    #    ACTUALIZACION TABLA DE SIMBOLOS  #
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = p[4]  # Obtenemos el tipo de la variable
    #print("p[1] = ",p[1],"p[2] = ",p[2],"p[3] = ",p[3],"p[4] = ",p[4], "p[5] = ",p[5],"p[6] = ",p[6])
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Array Already declared!")
    else:
        # Tabla de simbolos
        tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
        tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
        tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
        Simbol_Index = Simbol_Index + 1 # Incrementamos la posicion de la tabla de simbolos
        # Cuadruplos
        operand1 = pila_operandos.pop()
        result   = simbolo     
        pila_operandos.append(result)
        cuadruplos('=',operand1," ", result)
#   ACTUALIZACION DE VARIABLES TIPO ARREGLO     #
def p_act_Arr(p):
    '''
    act_Arr : ID dimension ASSIGN expression SEMICOLON
    '''
                                                          # NOMBRE_VAR DIMENSION = V_int/V_string/V_float/variable ;
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} array is not declared!")
    operand1 = pila_operandos.pop()
    result   = simbolo
    if not simbolo in pila_operandos:     
        pila_operandos.append(result)
        cuadruplos('=',operand1," ", result)
    else:
        cuadruplos('=',operand1," ", result)
#   DECLARACION - DIMENSIONES POSIBLES Y SU COTENIDO
def p_dimension(p):
    '''
    dimension : LCAS expression RCAS
              | LCAS expression RCAS LCAS expression RCAS
    '''
                                                          # Dimensiones con indices, tanto de tipo entero o variables
                                                          # ARR[V_int/ID], ARR[V_int/ID][V_int/ID] Maximo 2 dimensiones

#   TIPOS DE DATOS    #
def p_type(p):
    '''
    type : INT
         | FLT
         | STRING
    '''
                                                          # Tipos de datos -> INT, FLT, STRING 
    p[0] = p[1] # Necesario para que se identifique el tipo en la tabla de simbolos

#   FUNCION WRITE (PRINT)   #
def p_write(p):
    '''
    f_write : WRITE LPAR expression RPAR SEMICOLON
            | WRITE LPAR string_value RPAR SEMICOLON

    '''
                                                          # WRITE(ID/V_string/V_int,V_float)

#   FUNCION READ   #
def p_read(p):
    '''
    f_read : READ LPAR expression RPAR SEMICOLON
           | READ LPAR string_value RPAR SEMICOLON
    '''
                                                          # READ(ID/V_string/V_int,V_float)
# Operaciones aritmeticas
def p_suma_aritmetica(p):
    '''
    expression : expression PLUS expression 
    '''
    #print("Operando 2 antes   = ",operand2)    
    #print("Pila antes = ",pila_operandos)
    operand2 = pila_operandos.pop()
    #print("Operando 2 despues = ",operand2)
    #print("Operando 1 antes   = ",operand1)
    operand1 = pila_operandos.pop()
    #print("Operando 1 despues = ",operand1)
    #print("Operando result antes = ", result)
    result = temporales.pop()     
    #print("Operando result despues = ", result)
    pila_operandos.append(result)
    cuadruplos('+',operand1, operand2, result)

def p_resta_aritmetica(p):
    '''
    expression : expression MINUS expression 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('-',operand1, operand2, result)

def p_mpy_aritmetica(p):
    '''
    expression : expression TIMES expression 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('*',operand1, operand2, result)

def p_div_aritmetica(p):
    '''
    expression : expression DIVIDE expression 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('/',operand1, operand2, result)

def p_constante_expr_aritmetica(p):
    'expression : constante'
    p[0] = p[1]     # Nos permite operaciones recusrivas e infinitas

def p_agrupar(p):
    '''
    constante : LPAR expression RPAR
    '''
    p[0] = p[2]     # Nos quedamos con la expresion sin el parentesis

def p_agrupar_logicos(p):
    '''
    constante : LPAR comp_expression RPAR
    '''
    p[0] = p[2]     # Nos quedamos con la expresion sin el parentesis

#   Expresiones COMPARATIVAS   #
def p_comp_expression_equal(p):
    '''
    comp_expression : expression EQUAL expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('==',operand1, operand2, result)

def p_comp_expression_gt(p):
    '''
    comp_expression : expression GT expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('>',operand1, operand2, result)

def p_comp_expression_lt(p):
    '''
    comp_expression : expression LT expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('<',operand1, operand2, result)

def p_comp_expression_gteq(p):
    '''
    comp_expression : expression GTEQ expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('>=',operand1, operand2, result)

def p_comp_expression_lteq(p):
    '''
    comp_expression : expression LTEQ expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('<=',operand1, operand2, result)

def p_comp_expression_noteq(p):
    '''
    comp_expression : expression NOTEQ expression
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('!=',operand1, operand2, result)

def p_comp_expression_logicas(p):
    '''
    comp_expression : comp_expression logicas comp_expression
    '''

#   Expresiones LOGICAS         #
def p_logicas_and(p):
    '''
    logicas :  AND 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('&',operand1, operand2, result)

def p_logicas_or(p):
    '''
    logicas :  OR 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('|',operand1, operand2, result)

def p_logicas_not(p):
    '''
    logicas :  NOT 
    '''
    operand2 = pila_operandos.pop()
    operand1 = pila_operandos.pop()
    result = temporales.pop()     
    pila_operandos.append(result)
    cuadruplos('!',operand1, operand2, result)

def p_constante_expr_logicas(p):
    'comp_expression : constante'
    p[0] = p[1]     # Nos permite operaciones recusrivas e infinitas

#   CONSTANTES NUMERICAS para ser utilizadas en las expresiones
def p_constante_num(p):
    '''
    constante : INTV
              | FLTV
    '''
    pila_operandos.append(p[1])
#   CONSTANTES DE ID para ser utilizadas en las expresiones, como variables y arreglos
def p_constante_ID(p):
    '''
    constante : ID
              | ID dimension
    '''
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado
        compilador.exit(f"{simbolo} ID is not declared!")
    else:
        pila_operandos.append(p[1])


def p_stringV(p):
    '''
    string_value : STRINGV
    '''
#   LLAMADA A FUNCIONES     #
def p_call_func(p):
    '''
    c_func : ID LPAR RPAR SEMICOLON 
    '''
                                                          # Sintaxis para ir a una funcion ID(); seguido de la declaracion de la funcion
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, en este caso la funcion
        compilador.exit(f"{simbolo} Function is not declared!")

#   Formato de la funcion
def p_func_dec(p):
    '''
    dec_func : ID LPAR RPAR LBRK estatutos  RBRK
    ''' 
                                                          # Sintaxis de la estructura de una funcion ID(){ estatutos }
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = "Func"  # Obtenemos el tipo de la variable
    #print("p[1] = ",p[1],"p[2] = ",p[2],"p[3] = ",p[3],"p[4] = ",p[4], "p[5] = ",p[5],"p[6] = ",p[6])
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Function Already declared!")
    else:
        tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
        tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
        tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
        Simbol_Index = Simbol_Index + 1 # Incrementamos la posicion de la tabla de simbolos


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
    with open("cuadruplos_prueba.txt",  encoding="utf8") as f:
        file = f.read()
    parser.parse(file)
except EOFError:
    pass
print("Fin de lectura")
#print("Tabla de simbolos Final:")
#print(tabla_de_simbolos)
print("Pila de operandos Final:")
print(pila_operandos)
