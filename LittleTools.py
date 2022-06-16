# TRADUCCION DE CICLOS E IF:
pila_saltos = [] # Almacenamos los saltos del programa

#TRADUCCION FUNCIONES
pila_saltos_funciones = [] # Almacena los saltos que deben ser ejecutados para revisar funciones
pila_funciones = {} # Auxiliar, no tabla de simbolos
flag_func = True    # flag que identifica la primera funcion que nos llevara a el MAIN
pila_saltos_funciones_aux = [] # Contiene las direcciones de retorno de los call
pila_end_procedure = [] # Contiene las direcciones de donde saltamos de los modulos

# Variables dimensionadas
tamano_total = 0        # Contiene el tamaño total de espacio que necesita un arreglo

def updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index):
    tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
    tabla_de_simbolos[simbolo]["Value"] = None

    Simbol_Index = Simbol_Index + 1 # Incrementamos la posicion de la tabla de simbolos

    return Simbol_Index

def fillSimbolTable(simbolo,tabla_de_simbolos,valor):
    tabla_de_simbolos[simbolo]["Value"] = valor

# CUADRUPLOS
temporales = []     # Variable para ingresar los temporales
temporalesCopy = [] # Copia de los temporales
temporalCounter = 1 # Variable para contar el numero de temporales (T1 inicial)
sTemporal = "T"     # String constante para los temporales
pila_cuadruplos = [] # Pila para guardar los cuadruplos generados 
contador_cuadruplos = 0 # contador de los cuadruplos generados
#temporalesCopyArr = []
# Funcion que permite generar cuadruplos

def genTemporales():
    global temporalCounter
    temporal = sTemporal + str(temporalCounter) # Creamos un temporal tipo String
    temporales.append(temporal)                 # Añadimos al arreglo de temporales el string 
    temporalesCopy.append(temporal)             # Creamos una copia que no sera Pop() sus valores
    #temporalesCopyArr.append(temporal)             # Creamos una copia que no sera Pop() sus valores

    temporalCounter = temporalCounter + 1       # Aumentamos en 1 nuestro contador de temporales


def genCuadruplos(simbolo,operation,pila_operandos):
    if (operation == "="):  # Validacion de Creacion / asignacion
        global contador_cuadruplos
        operand1 = pila_operandos.pop()
        result   = simbolo
        if not simbolo in pila_operandos:                 # Verificamos si el simbolo ya habia sido declarado, para no meterlo en la pila mas veces
            pila_operandos.append(result)        
            cuadruplo = [operation, operand1,None, result] # Armamos el cuadruplo
            #print("Cuadruplo -> ",cuadruplo)              # Imprimimos el cuadruplo
            pila_cuadruplos.append(cuadruplo)
            contador_cuadruplos = contador_cuadruplos + 1
            #print(pila_operandos)
        else:
            cuadruplo = [operation, operand1,None, result] # Armamos el cuadruplo
            #print("Cuadruplo -> ",cuadruplo)              # Imprimimos el cuadruplo
            pila_cuadruplos.append(cuadruplo)
            contador_cuadruplos = contador_cuadruplos + 1

    elif(operation == "+" or operation == "-" or operation == "*" or operation == "/" or operation == "^"): # Validacion Aritmetica
        operand2 = pila_operandos.pop()
        operand1 = pila_operandos.pop()
        genTemporales()                                     # Generamos un temporal
        result = temporales.pop()     
        pila_operandos.append(result)
        cuadruplo = [operation, operand1, operand2, result] # Armamos el cuadruplo
        #print("Cuadruplo -> ",cuadruplo)                   # Imprimimos el cuadruplo
        pila_cuadruplos.append(cuadruplo)
        contador_cuadruplos = contador_cuadruplos + 1
        #print(pila_operandos)
    
    elif(operation == "&" or operation == "==" or operation == "!=" or 
        operation == ">" or operation == ">=" or operation == "<=" or
        operation == "|" or operation == "<"): # Validacion logica

        operand2 = pila_operandos.pop()
        operand1 = pila_operandos.pop()
        genTemporales()                                     # Generamos un temporal
        result = temporales.pop()    
        pila_operandos.append(result)
        cuadruplo = [operation, operand1, operand2, result] # Armamos el cuadruplo
        #print("Cuadruplo -> ",cuadruplo)                    # Imprimimos el cuadruplo
        pila_cuadruplos.append(cuadruplo)
        contador_cuadruplos = contador_cuadruplos + 1
        #print(pila_operandos)

    elif(operation == "READ"):
        operand1 = pila_operandos.pop()
        cuadruplo = [operation, operand1,None, None] # Armamos el cuadruplo
        #print("Cuadruplo -> ",cuadruplo)              # Imprimimos el cuadruplo
        pila_cuadruplos.append(cuadruplo)
        contador_cuadruplos = contador_cuadruplos + 1
        
    elif(operation == "WRITE"):
        operand1 = pila_operandos.pop()
        cuadruplo = [operation, operand1,None, None] # Armamos el cuadruplo
        #print("Cuadruplo -> ",cuadruplo)              # Imprimimos el cuadruplo
        pila_cuadruplos.append(cuadruplo)
        contador_cuadruplos = contador_cuadruplos + 1
    
    else:
        print(operation)
        print("error detected! bad logic!!")

# FUNCIONES IF -TRADUCCION-
def genCuadruplos_if(pila_operandos):
    global contador_cuadruplos
    operand1 = pila_operandos.pop()               # Recuperamos el operando
    genTemporales()                               # Generamos un temporal
    result = temporales.pop()                     # Guardamos el temporal como resultado
    pila_operandos.append(result)                 # Añadimos a la pila de operandos el resultado
    pila_saltos.append(contador_cuadruplos)       # Añadimos el cuadruplo a saltar en su pila
    cuadruplo = ["GOTOF", operand1,None,None]   # Armamos el cuadruplo
    pila_cuadruplos.append(cuadruplo)             # Añadimos el cuadruplo a la pila de cuadruplos
    contador_cuadruplos = contador_cuadruplos + 1 # Aumentamos el contador de cuadruplos

def genCuadruplos_if_then():
    global contador_cuadruplos
    salto = pila_saltos.pop()                           # Obtenemos el salto
    pila_cuadruplos[salto][3] = contador_cuadruplos + 1 # Actualizamos el valor del salto de cuadruplo a saltar          
    pila_saltos.append(contador_cuadruplos)             #
    cuadruplo = ["GOTO",None,None,None] # Armamos el cuadruplo
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1

def endifgoto():
    global contador_cuadruplos
    salto = pila_saltos.pop()
    pila_cuadruplos[salto][3] = contador_cuadruplos

# FUNCIONES FOR -TRADUCCION-

def genCuadruplos_for(pila_operandos):
    global contador_cuadruplos
    operand1 = pila_operandos.pop()               # Recuperamos el operando
    genTemporales()                               # Generamos un temporal
    result = temporales.pop()                     # Guardamos el temporal como resultado
    pila_operandos.append(result)                 # Añadimos a la pila de operandos el resultado
    pila_saltos.append(contador_cuadruplos)       # Añadimos el cuadruplo a saltar en su pila
    cuadruplo = ["GOTOF", operand1,None,None]     # Armamos el cuadruplo
    pila_cuadruplos.append(cuadruplo)             # Añadimos el cuadruplo a la pila de cuadruplos
    contador_cuadruplos = contador_cuadruplos + 1 # Aumentamos el contador de cuadruplos
 
def genCuadruplos_endfor():
    global contador_cuadruplos    
    salto = pila_saltos.pop()
    cuadruplo = ["GOTO",None,None,None]
    pila_cuadruplos.append(cuadruplo)
    pila_cuadruplos[contador_cuadruplos][3] = salto - 1
    contador_cuadruplos = contador_cuadruplos + 1 # Aumentamos el contador de cuadruplos
    pila_saltos.append(salto)
    

def genCuadruplos_plus_for(aux_for,operation,pila_operandos):
    global contador_cuadruplos
    cuadruplo = [operation, aux_for, 1, aux_for] # Armamos el cuadruplo
    #print("Cuadruplo -> ",cuadruplo)                    # Imprimimos el cuadruplo
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1   

def genCuadruplos_endingfor():
    global contador_cuadruplos
    salto = pila_saltos.pop()
    pila_cuadruplos[salto][3] = contador_cuadruplos


# FUNCIONES DO WHILE -TRADUCCION-
def genCuadruplos_do_while(pila_operandos):
    global contador_cuadruplos
    resultado = pila_operandos.pop()
    pila_saltos.append(contador_cuadruplos)
    cuadruplo = ["GOTOF",resultado,None,None]
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1
    print("PILA SE DALTOS DO_WHILE",pila_saltos)


def genCuadruplos_while(pila_operandos):
    global contador_cuadruplos
    pila_saltos.append(contador_cuadruplos)
    print("PILA SE DALTOS WHILE",pila_saltos)

    #contador_cuadruplos = contador_cuadruplos + 1
#     print("entro al while",pila_saltos)
#     global contador_cuadruplos
#     pila_saltos.append(contador_cuadruplos) # Guardamos la posicion donde estamos actualmente y rellenar
#     result =  pila_operandos.pop() # recuperamos el resultado generado por la expresion de log_exp
#     cuadruplo = ["GOTOF",result,None,None]
#     pila_cuadruplos.append(cuadruplo)
#     print("salto GOTOF -> ",pila_saltos)
#     print(pila_saltos)
#     contador_cuadruplos = contador_cuadruplos + 1


def genCuadruplos_whilethen():
    global contador_cuadruplos
    print("PILA SE DALTOS WHILETHE",pila_saltos)
    f = pila_saltos.pop()
    retorno = pila_saltos.pop()
    cuadruplo = ["GOTO",None,None,retorno-1]
    pila_cuadruplos.append(cuadruplo)
    pila_cuadruplos[f][3] = contador_cuadruplos
    contador_cuadruplos = contador_cuadruplos + 1
#     global contador_cuadruplos
#     salto = pila_saltos.pop() # obtenemos donde saltamos y regresamos a donde hicimos su expresion
#     cuadruplo = ["GOTO",None,None,salto-1] # Generamos cuadruplo
#     pila_cuadruplos.append(cuadruplo) # Añadimos cuadruplo a nuestra pila
#     pila_saltos.append(contador_cuadruplos) # Mandamos a la pila nuestra ubicacion
#     contador_cuadruplos = contador_cuadruplos + 1 # actualizamos contador
#     pila_cuadruplos[salto][3] = contador_cuadruplos # completamos cuadruplo

#     pila_saltos.append(salto)
#     salto = pila_saltos.pop() # obtenemos la posición a rellenar
#     print("salto GOTO -> ",pila_saltos)
#     print(pila_saltos)
#     pila_cuadruplos[salto][3] = contador_cuadruplos # completamos cuadruplo
#     print("salio al while",pila_saltos)

def genCuadruplos_endingwhile():
    global contador_cuadruplos
    salto = pila_saltos.pop() # obtenemos la posición a rellenar
    pila_cuadruplos[salto][3] = contador_cuadruplos # completamos cuadruplo

#   FUNCIONES
def genCuadruploinit_dec_func(simbolo):
    global contador_cuadruplos
    # Solo el la primera funcion nos genera un goto al main
    print("Pila Saltos funcionesc= ",len(pila_funciones))
    if(len(pila_funciones) < 1): # Verificamos si es la primera funcion que existe
        pila_saltos_funciones.append(contador_cuadruplos) # asignamos posición actual del cuadruplo a la pila de saltos
        cuadruplo = ["GOTOS",None,None,None] # Aun falta Llenar su espacio de destino (para la primera funcion)
        pila_cuadruplos.append(cuadruplo)        
        # Guardamos datos de la funcion
        pila_funciones[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
        pila_funciones[simbolo]["Salto"] = contador_cuadruplos # Guardamos la posicion de su cuadruplo

        contador_cuadruplos = contador_cuadruplos + 1

        
    pila_saltos_funciones.append(contador_cuadruplos) # Guardamos donde salto la funcion
    pila_funciones[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
    pila_funciones[simbolo]["Salto"] = contador_cuadruplos # Guardamos la posicion de su cuadruplo

#   FUNCIONES   #

def genCuadruplo_dec_func():
    global contador_cuadruplos
    pila_saltos_funciones.append(contador_cuadruplos)
    cuadruplo = ["Endprocedure",None,None,None] # Aun falta Llenar su espacio de destino de Main
    pila_end_procedure.append(contador_cuadruplos)
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1
    
def fill_functionsCuadruplos_main(posicionMain):
    pila_cuadruplos[pila_saltos_funciones[0]][3] = posicionMain # Actualizamos el valor con la posicion del main

def fill_functionsCuadruplos():
    # Llenamos las llamadas a funcion
        #for x in range (len(pila_end_procedure)):
        valuemodif = pila_saltos_funciones_aux.pop()
        cuadMod = pila_end_procedure[0]
        pila_end_procedure.pop(0)
        pila_cuadruplos[cuadMod][3] = valuemodif + 1 # Actualizamos el valor con la posicion del main


def gen_callCuadruplo(simbolo):
    global contador_cuadruplos
    # Lo buscamos en el diccionario de funciones
    Posicion = pila_funciones[simbolo]["Salto"] # Guardamos la posicion de su cuadruplo
    cuadruplo = ["CALL",None,None,Posicion]
    pila_cuadruplos.append(cuadruplo)
    pila_saltos_funciones.append(contador_cuadruplos)
    pila_saltos_funciones_aux.append(contador_cuadruplos)
    contador_cuadruplos = contador_cuadruplos + 1

def endProgram():
    global contador_cuadruplos
    cuadruplo = ["Endprogram",None,None,None]
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1

#   FUNCIONES PARA LOS ARREGLOS     #
#   CUANDO SE DECLARAN INICIALMENTE #
def genCuad_Arr1D(pila_operandos,simbolo,tipo,tabla_de_simbolos,Simbol_Index):

    global contador_cuadruplos
    Resultado_Indice = pila_operandos.pop()
    print("Resultado indice ",Resultado_Indice)
    cuadruplo = ["VER",Resultado_Indice,0,Resultado_Indice]
    pila_cuadruplos.append(cuadruplo)
    contador_cuadruplos = contador_cuadruplos + 1
    #Actualizamos tabla de simbolos 1D:
    tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
    tabla_de_simbolos[simbolo]["Value"] = None
    Simbol_Index = Simbol_Index + 1
    return Simbol_Index
    


def createSpaceInMemory(simbolo,dimension1,dimension2,dimension3,memArreglos):
    global tamano_total
    tamano_total = dimension1*dimension2*dimension3    # Obtenemos el tamaño total de espacios a utilizar 
    
    print("Tamaño total -> ",tamano_total) 
    for x in range(tamano_total):                         # Creamos el numero n de espacios en el arreglo
        memArreglos.append(simbolo)                       # Simbolicamente agregamos su asignacion en memoria
    #   Generamos Informacion en tabla de simbolos func updateSimbolTable_ARR, se llama desde el main

def updateSimbolTable_ARR_1D(simbolo,tipo,tabla_de_simbolos,Simbol_Index,base,dimension1,dimension2,dimension3):
    global tamano_total
    base = Simbol_Index                                 # aumentamos la base al tamano_total + 1
    lim_Inf = base                                      # Generamos nuestro limite inferior             
    lim_Sup = Simbol_Index + tamano_total - 1           # Generamos nuestro limite superior
    tabla_de_simbolos[simbolo] = {}                     # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["1D"] = dimension1       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo           # Guardamos en el diccionario el tipo de la variable
    tabla_de_simbolos[simbolo]["Base"] = base           # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_Inf"] = lim_Inf     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_sup"] = lim_Sup     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["M"] = tamano_total      # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Array"] = True
    Simbol_Index = Simbol_Index + tamano_total    # Incrementamos la posicion de la tabla de simbolos
    return Simbol_Index

def updateSimbolTable_ARR_2D(simbolo,tipo,tabla_de_simbolos,Simbol_Index,base,dimension1, dimension2, dimension3):
    global tamano_total
    base = Simbol_Index                                 # aumentamos la base al tamano_total + 1
    lim_Inf = base                                      # Generamos nuestro limite inferior             
    lim_Sup = Simbol_Index + tamano_total - 1           # Generamos nuestro limite superior
    tabla_de_simbolos[simbolo] = {}                     # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["1D"] = dimension1       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["2D"] = dimension2       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo           # Guardamos en el diccionario el tipo de la variable
    tabla_de_simbolos[simbolo]["Base"] = base           # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_Inf"] = lim_Inf     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_sup"] = lim_Sup     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["M"] = tamano_total      # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["m1"] = dimension2*dimension3     # Guardamos la posicion en la tabla de simbolos 

    tabla_de_simbolos[simbolo]["Array"] = True
    Simbol_Index = Simbol_Index + tamano_total    # Incrementamos la posicion de la tabla de simbolos
    return Simbol_Index

def updateSimbolTable_ARR_3D(simbolo,tipo,tabla_de_simbolos,Simbol_Index,base,dimension1, dimension2, dimension3):
    global tamano_total
    base = Simbol_Index                                 # aumentamos la base al tamano_total + 1
    lim_Inf = base                                      # Generamos nuestro limite inferior             
    lim_Sup = Simbol_Index + tamano_total - 1           # Generamos nuestro limite superior
    tabla_de_simbolos[simbolo] = {}                     # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["1D"] = dimension1       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["2D"] = dimension2       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["3D"] = dimension3       # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo           # Guardamos en el diccionario el tipo de la variable
    tabla_de_simbolos[simbolo]["Base"] = base           # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_Inf"] = lim_Inf     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Lim_sup"] = lim_Sup     # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["M"] = tamano_total      # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["m1"] = dimension2*dimension3     # Guardamos la posicion en la tabla de simbolos 
    tabla_de_simbolos[simbolo]["m2"] = dimension3*1     # Guardamos la posicion en la tabla de simbolos 
    tabla_de_simbolos[simbolo]["Array"] = True
    Simbol_Index = Simbol_Index + tamano_total    # Incrementamos la posicion de la tabla de simbolos
    return Simbol_Index
