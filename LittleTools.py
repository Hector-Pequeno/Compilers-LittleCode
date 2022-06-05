# TRADUCCION DE CICLOS (IF):

pila_saltos = [] # Almacenamos los saltos del programa

def updateSimbolTable(simbolo,tipo,tabla_de_simbolos,Simbol_Index):
    tabla_de_simbolos[simbolo] = {} # Nos permite crear un diccionario de tipo NESTED
    tabla_de_simbolos[simbolo]["Index"] = Simbol_Index # Guardamos la posicion en la tabla de simbolos
    tabla_de_simbolos[simbolo]["Type"] = tipo # Guardamos en el diccionario el tipo de la variable
    Simbol_Index = Simbol_Index + 1 # Incrementamos la posicion de la tabla de simbolos
    return Simbol_Index

# CUADRUPLOS
temporales = []     # Variable para ingresar los temporales
temporalCounter = 1 # Variable para contar el numero de temporales (T1 inicial)
sTemporal = "T"     # String constante para los temporales
pila_cuadruplos = [] # Pila para guardar los cuadruplos generados 
contador_cuadruplos = 0 # contador de los cuadruplos generados

# Funcion que permite generar cuadruplos
def genTemporales():
    global temporalCounter
    temporal = sTemporal + str(temporalCounter) # Creamos un temporal tipo String
    temporales.append(temporal)                 # Añadimos al arreglo de temporales el string 
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

            #print(pila_operandos)
    elif (operation == "++" or operation == "--"):  # Validacion de Creacion / asignacion
        operand1 = simbolo
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
            #print(pila_operandos)
    elif(operation == "+" or operation == "-" or operation == "*" or operation == "/"): # Validacion Aritmetica
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

    elif(operation == "&" or operation == "==" or operation == "!=" or 
        operation == ">" or operation == ">=" or operation == "<=" or 
        operation == "|" or operation == "!" or operation == "<"): # Validacion logica

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




    #Funciona para el IF
    elif(operation == "GOTOF"):
        operand1 = pila_operandos.pop()               # Recuperamos el operando
        genTemporales()                               # Generamos un temporal
        result = temporales.pop()                     # Guardamos el temporal como resultado
        pila_operandos.append(result)                 # Añadimos a la pila de operandos el resultado
        pila_saltos.append(contador_cuadruplos)       # Añadimos el cuadruplo a saltar en su pila
        cuadruplo = [operation, operand1,None,None]   # Armamos el cuadruplo
        pila_cuadruplos.append(cuadruplo)             # Añadimos el cuadruplo a la pila de cuadruplos
        contador_cuadruplos = contador_cuadruplos + 1 # Aumentamos el contador de cuadruplos
 
    elif(operation == "GOTO"):
        salto = pila_saltos.pop()                           # Obtenemos el salto
        pila_cuadruplos[salto][3] = contador_cuadruplos + 1 # Actualizamos el valor del salto de cuadruplo a saltar          
        pila_saltos.append(contador_cuadruplos)             # Añadi
        cuadruplo = [operation,None,None,None] # Armamos el cuadruplo
        pila_cuadruplos.append(cuadruplo)
        contador_cuadruplos = contador_cuadruplos + 1

    else:
        print(operation)
        print("error detected! bad logic!!")

def endifgoto():
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
    cuadruplo = ["GOTOF", operand1,None,None]   # Armamos el cuadruplo
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
    
def genCuadruplos_endingfor():
    salto = pila_saltos.pop()
    global contador_cuadruplos
    pila_cuadruplos[salto][3] = contador_cuadruplos

# FUNCIONES DO WHILE -TRADUCCION-

def genCuadruplos_while():
    global contador_cuadruplos
    pila_saltos.append(contador_cuadruplos) # Guradamos el inicio del DO

def genCuadruplos_endingwhile(pila_operandos):
    global contador_cuadruplos
    salto = pila_saltos.pop()
    operand1 = pila_operandos.pop()               # Recuperamos el operando
    pila_saltos.append(contador_cuadruplos)       # Añadimos el cuadruplo a saltar en su pila
    cuadruplo = ["GOTOF", operand1,None,salto]   # Armamos el cuadruplo
    pila_cuadruplos.append(cuadruplo)             # Añadimos el cuadruplo a la pila de cuadruplos
    contador_cuadruplos = contador_cuadruplos + 1 # Aumentamos el contador de cuadruplos
 
