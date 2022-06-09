import analizador_lexico_A01246364 as myLexer
import LittleTools
import ply.yacc as yacc
import sys as compilador

# Obtenemos los tokens
tokens = myLexer.tokens

# Constantes
DUMMY = 0 # Constante de envio, para completar funciones con argumentos
END_PROGRAM_FLAG = 0 # Constante que detiene la lectura de cuadruplos.
#   INICIO TABLA DE SIMBOLOS   #
tabla_de_simbolos = {} # Lista vacia, donde seran guardados nuestros simbolos
Simbol_Index = 0

#   CUADRUPLOS      #
Append_Flag = 1     # Bandera para verificar si es necesario volverlo a meter a la pila de operandos, 1 - SI SE METE, 0 - NO SE METE
pila_operandos = [] # Arreglo de operandos
aux_for = 0         # Nos funciona para guardar la variable a incrementar en el ciclo for
flag_funciones = False # Verificamos si existen funciones
# Ejecucion
pc = 0

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
    program : program dec_func
            | program main
            | program dec_Var
            | empty
    '''
                                                          # funcion_n(){estatutos}  y|o  main(){ estatutos }  y|o vacio
def p_main(p):
    '''
    main : mainBegin estatutos RBRK
    '''
                                                          # main(){ estatutos }
    #######     
    if flag_funciones == 1:     
        LittleTools.endProgram()          # END PROGRAM

def p_mainBegin(p):
    '''
    mainBegin : MAIN LPAR RPAR LBRK
    '''
    global flag_funciones
    posicionMain = LittleTools.contador_cuadruplos
    if flag_funciones == 1:
        LittleTools.fill_functionsCuadruplos_main(posicionMain)  
    
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
              | estatutos log_exp SEMICOLON
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

#   DECLARACION ESTATUTO IF     #
def p_estatuto_if(p):
    '''
    e_if : first_if estatutos second_if estatutos ENDIF
         | first_if estatutos ENDIF
    '''
    LittleTools.endifgoto()

def p_estatuto_if_first(p):
    '''
    first_if : IF LPAR log_exp RPAR THEN
    '''
    LittleTools.genCuadruplos_if(pila_operandos)     # Cuadruplos de entrada al IF (GOTOF)
    
def p_estatuto_if_second(p):
    '''
    second_if : ELSE THEN
    '''
    LittleTools.genCuadruplos_if_then()


#   DECLARACION ESTATUTOS DO WHILE    #
def p_estatuto_while(p):
    '''
    e_while : first_while estatutos second_while
    '''
    LittleTools.genCuadruplos_endingwhile()


def p_estatuto_first_while(p):
    '''
    first_while : WHILE LPAR log_exp RPAR THEN  
    '''
    LittleTools.genCuadruplos_while(pila_operandos)
    

def p_estatuto_second_while(p):
    '''
    second_while : ENDWHILE
    '''
    LittleTools.genCuadruplos_whilethen()


#   DECLARACION ESTATUTOS   FOR    #
def p_estatuto_for(p):
    '''
    e_for : e_for_first e_for_second
    '''
    global aux_for
    LittleTools.genCuadruplos_endingfor()

def p_estatuto_for_first(p):
    '''
    e_for_first : FOR LPAR act_Var_for RPAR TO INTV
                | FOR LPAR act_Var_for RPAR TO ID
    '''
    simbolo = p[6]
    pila_operandos.append(simbolo) # Agregamos operando a la pila 
    LittleTools.genCuadruplos(DUMMY,"<",pila_operandos)
    LittleTools.genCuadruplos_for(pila_operandos)     # Cuadruplos de entrada al IF (GOTOF)


def p_estatuto_for_second(p):
    '''
    e_for_second : THEN estatutos ENDFOR
    '''
    global aux_for
    pila_operandos.append(aux_for)
    LittleTools.genCuadruplos_plus_for(aux_for,"+",pila_operandos)

    LittleTools.genCuadruplos_endfor() 

def p_act_Var_for(p):
    '''
    act_Var_for : ID ASSIGN INTV

    '''
    global aux_for
    simbolo = p[1]
    valor = p[3]
    aux_for = simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} is not declared!")
    # Generamos Cuadruplos
    pila_operandos.append(p[3])
    LittleTools.genCuadruplos(simbolo,"=",pila_operandos)
    pila_operandos.append(p[1]) # Agregamos el simbolo para poder realizar la comparacion contra la constante
    LittleTools.fillSimbolTable(simbolo,tabla_de_simbolos,valor)

def p_dec_Var(p):
    '''
    dec_Var : ID DOUBLEPOINT type ASSIGN expression SEMICOLON
            | ID DOUBLEPOINT type ASSIGN f_read 
    '''
                                                          # NOMBRE_VAR : INT/STRING/FLOAT  = V_int/V_string/V_float/variable ;
                                                          # NOMBRE_VAR : INT/FLOAT/STRING ;
                                                          # igualar a una expresion
    #    ACTUALIZACION TABLA DE SIMBOLOS  #
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = p[3]  # Obtenemos el tipo de la variable
    valor = p[5]
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Already declared!")
    else: 
        # Tabla de simbolos
        Simbol_Index = LittleTools.updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index)
        # Llamamos a la generacion de Cuadruplos
        LittleTools.genCuadruplos(simbolo,"=",pila_operandos)
        LittleTools.fillSimbolTable(simbolo,tabla_de_simbolos,valor)


def p_dec_Var_woI(p): # Variable sin inicializar
    '''
    dec_Var : ID DOUBLEPOINT type SEMICOLON
    '''
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = p[3]  # Obtenemos el tipo de la variable
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Already declared!")
    else: 
        # Tabla de simbolos
        Simbol_Index = LittleTools.updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index)

#   ACTUALIZACION DE VARIABLES  #
def p_act_Var(p):
    '''
    act_Var : ID ASSIGN expression SEMICOLON
            | ID ASSIGN f_read
    '''
                                                          # NOMBRE_VAR = V_int/V_string/V_float/variable ;
    simbolo = p[1] # Obtenemos el simbolo
    valor = p[3]
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} is not declared!")
    # Generamos Cuadruplos
    LittleTools.genCuadruplos(simbolo,"=",pila_operandos)
    LittleTools.fillSimbolTable(simbolo,tabla_de_simbolos,valor)



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
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Array Already declared!")
    else:
        # Tabla de simbolos
        Simbol_Index = LittleTools.updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index)
        
        # Cuadruplos
        #LittleTools.genCuadruplos(simbolo,"=",pila_operandos)

        
#   ACTUALIZACION DE VARIABLES TIPO ARREGLO     #
def p_act_Arr(p):
    '''
    act_Arr : ID dimension ASSIGN expression SEMICOLON
            | ID dimension ASSIGN f_read 
    '''
                                                          # NOMBRE_VAR DIMENSION = V_int/V_string/V_float/variable ;
    simbolo = p[1] # Obtenemos el simbolo
    valor = p[4]
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, para actualizarlo
        compilador.exit(f"{simbolo} array is not declared!")
   # Generamos Cuadruplos
    LittleTools.genCuadruplos(simbolo,"=",pila_operandos)
    LittleTools.fillSimbolTable(simbolo,tabla_de_simbolos,valor)

#   DECLARACION - DIMENSIONES POSIBLES Y SU COTENIDO
def p_dimension(p):
    '''
    dimension : LCAS expression_arr RCAS
              | LCAS expression_arr RCAS LCAS expression_arr RCAS
    '''
                                                          # Dimensiones con indices, tanto de tipo entero o variables
                                                          # ARR[V_int/ID], ARR[V_int/ID][V_int/ID] Maximo 2 dimensiones
#   Expresiones para arreglos   #
def p_suma_aritmetica_arr(p):
    '''
    expression_arr : expression_arr PLUS expression_arr 
    '''
    LittleTools.genCuadruplos(DUMMY,"+",pila_operandos)



def p_resta_aritmetica_arr(p):
    '''
    expression_arr : expression_arr MINUS expression_arr 
    '''
    LittleTools.genCuadruplos(DUMMY,"-",pila_operandos)


def p_mpy_aritmetica_arr(p):
    '''
    expression_arr : expression_arr TIMES expression_arr 
    '''
    LittleTools.genCuadruplos(DUMMY,"*",pila_operandos)

def p_div_aritmetica_arr(p):
    '''
    expression_arr : expression_arr DIVIDE expression_arr 
    '''
    LittleTools.genCuadruplos(DUMMY,"/",pila_operandos)

def p_constante_expr_aritmetica_arr(p):
    'expression_arr : constante_arr'
    p[0] = p[1]     # Nos permite operaciones recusrivas e infinitas

def p_agrupar_arr(p):
    '''
    constante_arr : LPAR expression_arr RPAR
    '''
    p[0] = p[2]     # Nos quedamos con la expresion sin el parentesis

def p_constante_num_arr(p):
    '''
    constante_arr : INTV
                  | FLTV
    '''
    pila_operandos.append(p[1])
#   CONSTANTES DE ID para ser utilizadas en las expresiones, como variables y arreglos
def p_constante_ID_arr(p):
    '''
    constante_arr : ID
                  | ID dimension
    '''
#   FIN EXPRESIONES ARREGLOS
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
    simbolo = p[3]
    LittleTools.genCuadruplos(simbolo,"WRITE",pila_operandos)

                                                          # WRITE(ID/V_string/V_int,V_float)
#   FUNCION READ   #
def p_read(p):
    '''
    f_read : READ LPAR ID RPAR SEMICOLON
    '''
                                                          # READ(ID/V_string/V_int,V_float)
    simbolo = p[3]
    pila_operandos.append(simbolo)
    if not simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} is not declared!")
    else:
        # Genereamos cuadruplo
        LittleTools.genCuadruplos(simbolo,"READ",pila_operandos)

# Operaciones aritmeticas
def p_suma_aritmetica(p):
    '''
    expression : expression PLUS expression 
    '''
    LittleTools.genCuadruplos(DUMMY,"+",pila_operandos)



def p_resta_aritmetica(p):
    '''
    expression : expression MINUS expression 
    '''
    LittleTools.genCuadruplos(DUMMY,"-",pila_operandos)


def p_mpy_aritmetica(p):
    '''
    expression : expression TIMES expression 
    '''
    LittleTools.genCuadruplos(DUMMY,"*",pila_operandos)

def p_div_aritmetica(p):
    '''
    expression : expression DIVIDE expression 
    '''
    LittleTools.genCuadruplos(DUMMY,"/",pila_operandos)

def p_constante_expr_aritmetica(p):
    'expression : constante'
    p[0] = p[1]     # Nos permite operaciones recusrivas e infinitas

def p_agrupar(p):
    '''
    constante : LPAR expression RPAR
    '''
    p[0] = p[2]     # Nos quedamos con la expresion sin el parentesis

#   Expresiones Logicas   #
#   EQUAL   #
def p_log_exp_eq(p):
    '''
    log_exp : log_exp EQUAL log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"==",pila_operandos)


#   NOT EQUAL
def p_log_exp_noteq(p):
    '''
    log_exp : log_exp NOTEQ log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"!=",pila_operandos)

#   GRATER THAN
def p_log_exp_gt(p):
    '''
    log_exp : log_exp GT log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,">",pila_operandos)

#   LESS THAN   
def p_log_exp_lt(p):
    '''
    log_exp : log_exp LT log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"<",pila_operandos)

#   GRATER THAN EQUAL
def p_log_exp_gteq(p):
    '''
    log_exp : log_exp GTEQ log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,">=",pila_operandos)

#   LOWER THAN EQUAL
def p_log_exp_lteq(p):
    '''
    log_exp : log_exp LTEQ log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"<=",pila_operandos)

#   AND
def p_log_exp_and(p):
    '''
    log_exp : log_exp AND log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"&",pila_operandos)

#   OR
def p_log_exp_or(p):
    '''
    log_exp : log_exp OR log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"|",pila_operandos)

#   NOT
def p_log_exp_not(p):
    '''
    log_exp : log_exp NOT log_exp
    '''
    LittleTools.genCuadruplos(DUMMY,"!",pila_operandos)

def p_log_agrupacion(p):
    '''
    log_exp : LPAR log_exp RPAR
    '''
    p[0] = p[2]     # Nos quedamos con la expresion sin el parentesis

def p_constante_expr_logicas(p):
    'log_exp : constante'
    p[0] = p[1]     # Nos permite operaciones recurSivas e infinitas

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
    pila_operandos.append(p[1])

#   LLAMADA A FUNCIONES     #
def p_call_func(p):
    '''
    c_func : ID LPAR RPAR SEMICOLON 
    '''
                                                          # Sintaxis para ir a una funcion ID(); seguido de la declaracion de la funcion
    simbolo = p[1] # Obtenemos el simbolo
    if not p[1] in tabla_de_simbolos:   # Verificamos si el simbolo se encuentra declarado, en este caso la funcion
        compilador.exit(f"{simbolo} Function is not declared!")
    # Generar cuadruplo para ir a las funciones
    LittleTools.gen_callCuadruplo(simbolo)
    LittleTools.fill_functionsCuadruplos()
#   Formato de la funcion
def p_func_dec(p):
    '''
    dec_func : dec_func_init dec_func_end RBRK
    ''' 
                                                          # Sintaxis de la estructura de una funcion ID(){ estatutos }
    global flag_funciones
    #genermos cuadruplos
    #pila_operandos.pop()
    LittleTools.genCuadruplo_dec_func()
    flag_funciones = True               # Activamos flag

def p_func_end(p):
    '''
    dec_func_end : LBRK estatutos
    
    '''
def p_func_int(p):
    '''
    dec_func_init : ID LPAR RPAR 
    ''' 
                                                          # Sintaxis de la estructura de una funcion ID(){ estatutos }
    global Simbol_Index # Nos permite utilizar la variable global dentro de la actualizacion de simbolos
    simbolo = p[1]  # Obtenemos el simbolo
    tipo = "Func"  # Obtenemos el tipo de la variable
    if simbolo in tabla_de_simbolos:
        compilador.exit(f"{simbolo} Function Already declared!")
    else:
        # Tabla de simbolos
        Simbol_Index = LittleTools.updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index)
        # Generamos su cuadruplo
        LittleTools.genCuadruploinit_dec_func(simbolo)

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
    with open("ejecucion_VS_if.txt",  encoding="utf8") as f:
        file = f.read()
    parser.parse(file)
except EOFError:
    pass

print("Fin de lectura")

print("\nTabla de simbolos Inicial:")
for key in tabla_de_simbolos:
    print(key, ' : ', tabla_de_simbolos[key])

print(" ")
print("Cuadruplos a Ejecutar:")
for i in range (len( LittleTools.pila_cuadruplos)):
    print(LittleTools.pila_cuadruplos[i])



# Restamos al contador de cuadruplos 1, para que este en el rango de la lista
# LittleTools.contador_cuadruplos -= 1
cuadruplos_Finales = LittleTools.pila_cuadruplos # Obtenemos la lista de cuadruplos
temporalesCopia = LittleTools.temporalesCopy     # Obtenemos la copia de los temporales
#resTemporales = []                  # Lista donde se guardan los valores de los temporales
resTemporales = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

print(temporalesCopia)
# Ciclo de revision de cuadruplos
print("\nInicio Ejecucion...")
print("\nOutput Consola:")

while pc < len(cuadruplos_Finales):
    cuadruplo_actual = cuadruplos_Finales[pc]   # Nos colocamos en el cuadruplo actual
    operation = cuadruplos_Finales[pc][0]       # Obtenemos la operacion del cuadruplo
    operando1 = cuadruplos_Finales[pc][1]       # Obtenemos primer operando
    operando2 = cuadruplos_Finales[pc][2]       # Obtenemos segundo operando
    resultado = cuadruplos_Finales[pc][3]       # Obtenemos donde se asigna el resultado
    # Verificamos si operando1 es una variable/temporal o una constante:
    if(operando1 in tabla_de_simbolos):
        if("Value" in tabla_de_simbolos[operando1]):          # Verificamos si existe un valor para la variable
            operando1 = tabla_de_simbolos[operando1]["Value"] # Obtenemos su valor
        else:
            compilador.exit("Variable sin inicializar")
    elif(operando1 in temporalesCopia):                       # Verificamos si el operando es un temporal
        fNum_operamdo1 = int(operando1[1])                    # Obtenemos la parte numerica del temporal
        operando1 = resTemporales[fNum_operamdo1-1]           # Guardamos en el operando 1 el resultado almacenado en resTemporados (indice correspondiente)

    # Verificamos si operando1 es una variable/temporal o una constante:
    if(operando2 in tabla_de_simbolos):                       # Se verifica a op2 como simbolo
        if("Value" in tabla_de_simbolos[operando2]):          # Verificamos si existe un valor para la variable
            operando2 = tabla_de_simbolos[operando2]["Value"] # Obtenemos su valor
        else:
            compilador.exit("Variable sin inicializar")
    elif(operando2 in temporalesCopia):                       # Verificamos si el operando es un temporal
        fNum_operamdo2 = int(operando2[1])                    # Obtenemos la parte numerica del temporal
        operando2 = resTemporales[fNum_operamdo2-1]           # Guardamos en el operando 1 el resultado almacenado en resTemporados (indice correspondiente)
    
    # Verificamos si el resultado es un temporal
    if(resultado in temporalesCopia):
        numTemporal = resultado[1]# Obtenemos el indice de temporal
        # Realizamos Operacion y guardamos en el numero que obtenemos del numTemporal[0] en el arreglo de resultados de temporales
        if operation == "=": 
            resTemporales[int(numTemporal)] = operando1
            pc += 1
        elif operation == "+":
            resTemporales[int(numTemporal)-1] = (operando1 + operando2)
            pc += 1
        elif operation == "-":
            resTemporales[int(numTemporal)-1] = (operando1 - operando2)
            pc += 1
        elif operation == "*":
            resTemporales[int(numTemporal)-1] = (operando1 * operando2)
            pc += 1
        elif operation == "/":
            resTemporales[int(numTemporal)-1] = (operando1 / operando2)
            pc += 1        
        elif operation == "==":
            resTemporales[int(numTemporal)-1] = (operando1 == operando2)
            pc += 1
        elif operation == ">":
            resTemporales[int(numTemporal)-1] = (operando1 > operando2)
            pc += 1
        elif operation == "<":
            resTemporales[int(numTemporal)-1] = (operando1 < operando2)
            pc += 1
        elif operation == ">=":
            resTemporales[int(numTemporal)-1] = (operando1 >= operando2)
            pc += 1
        elif operation == "<=":
            resTemporales[int(numTemporal)-1] = (operando1 <= operando2)
            pc += 1
        elif operation == "&":
            resTemporales[int(numTemporal)-1] = (operando1 and operando2)
            pc += 1
        elif operation == "|":
            resTemporales[int(numTemporal)-1] = (operando1 or operando2)
            pc += 1
#########
    else:
        if operation == "=":
            if (operando2 != None):
                if resultado in tabla_de_simbolos : #Si esta ya fue declarada
                    compilador.exit(f"La variable {resultado} ya fue declarada")
                else: 
                    tabla_de_simbolos[resultado] = {} #Creo un diccionario dentro
                    tabla_de_simbolos[resultado]["Index"] = Simbol_Index 
                    tabla_de_simbolos[resultado]["Type"]  = operando2
                    tabla_de_simbolos[resultado]["Value"] = operando1
                    Simbol_Index = Simbol_Index + 1
                    pc += 1
            else:
                if (not cuadruplo_actual[1] in cuadruplo_actual)and(not cuadruplo_actual[1] in cuadruplo_actual)and(not isinstance(cuadruplo_actual[1], int))and(not isinstance(cuadruplo_actual[1], float)):
                    compilador.exit(f"La variable {cuadruplo_actual} no ha sido declarada")
                else:
                    tabla_de_simbolos[resultado]["Value"] = operando1
                    pc += 1
                    
        elif operation == "+":
            tabla_de_simbolos[resultado]["Value"] = operando1 + operando2
            pc = pc + 1
        elif operation == "GOTO":
            pc = resultado
        elif operation == "GOTOF":
            if(operando1 == False):
                pc = resultado
            else:
                pc += 1
        elif operation == "Endprocedure":
            pc = resultado
        elif operation == "GOTOS":
            pc = resultado
        elif operation == "CALL":
            pc = resultado
        elif operation == "Endprogram":
            pc = pc+1
        elif operation == "WRITE":
            print(operando1)
            pc = pc+1
        elif operation == "READ":
            print(operando1)
            pc = pc+1
        else:
            pc += 1
print("\nTabla de simbolos Final:")
for key in tabla_de_simbolos:
    print(key, ' : ', tabla_de_simbolos[key])       
compilador.exit("\nCorrectly Execution :D")
 
