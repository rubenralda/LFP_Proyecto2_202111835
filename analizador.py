from clasesEtiquetas import AreaTexto, Boton, Check, Clave, Contenedor, Etiqueta, RadioBoton, Texto, This
#Recordatorio para el futuro: falta agregar mas errores al vector de errores pero detecta todos los 
#sintacticos y los lexicos faltaria detectar cuando faltan letras y regresar al estado inicial
#para agregar todo el lexema hasta el caracter erroneo, al vector de errores

class Errores:
    def __init__(self, tipo="", linea=0, columna=0, error="", descripcion=""):
        self.tipo = tipo
        self.fila = linea
        self.columna = columna
        self.error = error
        self.descripcion = descripcion


class Token:
    def __init__(self, lexema, categoria, fila, columna):
        self.lexema = lexema
        self.tipo = categoria
        self.fila = fila
        self.columna = columna


class Automatas:

    def __init__(self, cadena=""):
        self.cadena = cadena
        self.letras = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                       "m", "n", "ñ", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
        self.numeros = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")
        self.palabras_clave = ("controles", "etiqueta", "boton", "check", "radioboton",
                               "texto", "areatexto", "clave", "contenedor", "propiedades", "setcolorletra",
                               "settexto", "setalineacion", "setcolorfondo", "setmarcada", "setgrupo", "setancho",
                               "setalto", "colocacion", "setposicion", "add", "this", "true", "false", "centro", "izquierdo", "derecho")
        self.token = []
        self.errores = []
        self.etiquetas = []
        self.cuerpoPagina = This()
        self.control = ("etiqueta", "boton", "check", "radioboton",
                        "texto", "areatexto", "clave", "contenedor")
        self.metodo = ("setcolorletra",
                       "settexto", "setalineacion", "setcolorfondo", "setmarcada", "setgrupo", "setancho",
                       "setalto")
        self.parametro = ("10", "11", "2", "centro",
                          "izquierdo", "derecho", "true", "false")

    def lexico(self):
        lexema = ""
        estadoActual = 1
        columna = 1
        fila = 1
        while (len(self.cadena) > 0):
            char = self.cadena[0]
            match(estadoActual):
                case 1:
                    if char == "\n":
                        fila += 1
                        columna = 0
                        estadoActual = 2
                    elif char == " ":
                        estadoActual = 2
                    elif char == "\t":
                        estadoActual = 2
                    elif char == "/":
                        lexema += char
                        estadoActual = 3
                    elif char.lower() in self.letras:
                        lexema += char
                        estadoActual = 4
                    elif char in self.numeros:
                        lexema += char
                        estadoActual = 5
                    elif char == "<":
                        lexema += char
                        estadoActual = 6
                    elif char == "-":
                        lexema += char
                        estadoActual = 7
                    elif char == ";":  # estado 8 no se evalua su estado porque solo es un caracter
                        self.token.append(Token(char, "6", fila, columna))
                        estadoActual = 1
                    elif char == "(":  # estado 9 lo mismo de arriba
                        self.token.append(
                            Token(char, "7", fila, columna))
                        estadoActual = 1
                    elif char == ")":  # estado 10 lo mismo de arriba
                        self.token.append(
                            Token(char, "8", fila, columna))
                        estadoActual = 1
                    elif char == ".":  # estado 11 lo mismo de arriba
                        self.token.append(Token(char, "9", fila, columna))
                        estadoActual = 1
                    elif char == "\"":
                        lexema += char
                        estadoActual = 12
                    elif char == ",":  # estado 13
                        self.token.append(Token(char, "12", fila, columna))
                        estadoActual = 1
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "No se reconoce el token"))
                case 2:
                    if char == "\n":
                        fila += 1
                        columna = 0
                        estadoActual = 2
                    elif char == " ":
                        estadoActual = 2
                    elif char == "\t":
                        columna += 3
                        estadoActual = 2
                    else:
                        estadoActual = 1
                        continue
                case 3:
                    if char == "/":
                        lexema += char
                        estadoActual = 14
                    elif char == "*":
                        lexema += char
                        estadoActual = 15
                    else:
                        self.errores.append(Errores(
                            "Lexico", fila, columna, char, "Se esperaba \"/\" o \"*\", no se reconoce el token("+char+")"))
                case 4:
                    if char.lower() in self.letras or char in self.numeros:
                        estadoActual = 4
                        lexema += char
                    else:
                        if lexema.lower() in self.palabras_clave:
                            self.token.append(
                                Token(lexema, lexema.lower(), fila, columna))
                        else:
                            self.token.append(
                                Token(lexema, "2", fila, columna))  # identificador
                        lexema = ""
                        estadoActual = 1
                        continue
                case 5:
                    if char in self.numeros:
                        estadoActual = 5
                        lexema += char
                    else:
                        self.token.append(
                            Token(lexema, "10", fila, columna))  # numero
                        lexema = ""
                        estadoActual = 1
                        continue
                case 6:
                    if char == "!":
                        lexema += char
                        estadoActual = 16
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"!\""))
                case 7:
                    if char == "-":
                        lexema += char
                        estadoActual = 17
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"-\""))
                case 12:
                    if char.lower() in self.letras or char == " " or char in self.numeros:
                        estadoActual = 12
                        lexema += char
                    elif char == "\"":  # estado 18
                        lexema += char
                        self.token.append(
                            Token(lexema, "11", fila, columna))  # string
                        lexema = ""
                        estadoActual = 1
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \""))
                case 14:
                    if char.lower() in self.letras or char in self.numeros or char == " ":
                        lexema += char
                        estadoActual = 14
                    else:
                        self.token.append(
                            Token(lexema, "4", fila, columna))  # comentario simple
                        lexema = ""
                        estadoActual = 1
                        continue
                case 15:
                    if char.lower() in self.letras or char in self.numeros or char == "\n" or char == " " or char == "\t":
                        lexema += char
                        estadoActual = 15
                    elif char == "*":
                        lexema += char
                        estadoActual = 22
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"*\""))
                case 16:
                    if char == "-":
                        lexema += char
                        estadoActual = 19
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"-\""))
                case 17:
                    if char == ">":  # estado 20
                        lexema += char
                        self.token.append(
                            Token(lexema, "5", fila, columna))  # etiqueta cerradura
                        lexema = ""
                        estadoActual = 1
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \">\""))
                case 19:
                    if char == "-":  # estado 21
                        lexema += char
                        self.token.append(
                            Token(lexema, "3", fila, columna))  # etiqueta abertura
                        lexema = ""
                        estadoActual = 1
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"-\""))
                case 22:
                    if char == "/":  # estado 23
                        lexema += char
                        self.token.append(
                            Token(lexema, "1", fila, columna))  # comentario compuesto
                        lexema = ""
                        estadoActual = 1
                    else:
                        self.errores.append(
                            Errores("Lexico", fila, columna, char, "Se esperaba \"/\""))
            columna += 1
            self.cadena = self.cadena[1:]
        if lexema != "":
            if lexema.lower() in self.palabras_clave:
                self.token.append(Token(lexema, lexema.lower(), fila, columna))
            elif lexema in self.numeros:
                self.token.append(Token(lexema, "10", fila, columna))
            elif lexema[0] in self.letras:
                self.token.append(Token(lexema, "2", fila, columna))
            elif estadoActual == 23:
                self.token.append(Token(lexema, "1", fila, columna))
            elif estadoActual == 14:
                self.token.append(Token(lexema, "4", fila, columna))
            else:
                self.errores.append(
                    Errores("Lexico", fila, columna, lexema, "No se reconoce el token"))

    def crearEtiqueta(self, controlTemporal, idTemporal):
        match(controlTemporal.lower()):
            case "etiqueta":
                self.etiquetas.append(Etiqueta(idTemporal))
            case "boton":
                self.etiquetas.append(Boton(idTemporal))
            case "check":
                self.etiquetas.append(Check(idTemporal))
            case "radioboton":
                self.etiquetas.append(RadioBoton(idTemporal))
            case "texto":
                self.etiquetas.append(Texto(idTemporal))
            case "areatexto":
                self.etiquetas.append(AreaTexto(idTemporal))
            case "clave":
                self.etiquetas.append(Clave(idTemporal))
            case "contenedor":
                self.etiquetas.append(Contenedor(idTemporal))

    def sintactico(self):
        conteo = 0
        estado_actual = 0
        parametroMetodo = []
        parametroColo = []
        if self.token == None:
            return False
        for token in self.token:
            if token.tipo == "1" or token.tipo == "4":
                conteo += 1
                continue
            match(estado_actual):
                case 0:
                    if token.tipo == "3":  # abre
                        estado_actual = 1
                case 1:
                    if token.tipo == "controles":
                        estado_actual = 2
                    elif token.tipo == "propiedades":
                        estado_actual = 3
                    elif token.tipo == "colocacion":
                        estado_actual = 4
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "No se esperaba ese token"))
                        return False
                case 2:
                    if token.tipo in self.control:
                        controlTemporal = token.lexema
                        estado_actual = 5
                    elif token.tipo == "controles":
                        estado_actual = 6
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \"Controles\""))
                        return False
                case 3:
                    if token.tipo == "2":  # identificador
                        idpropiedad = token.lexema
                        estado_actual = 7
                    elif token.tipo == "propiedades":
                        estado_actual = 6
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba Propiedades"))
                        return False
                case 4:
                    if token.tipo == "2":  # identificador
                        idColocacion = token.lexema
                        estado_actual = 14
                    elif token.tipo == "this":
                        idColocacion = "this"
                        estado_actual = 15
                    elif token.tipo == "colocacion":
                        estado_actual = 6
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba Colocacion"))
                        return False
                case 5:
                    if token.tipo == "2":  # si es identificador
                        idTemporal = token.lexema
                        estado_actual = 8
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba un Identificador"))
                        return False
                case 6:
                    if token.tipo == "5":  # si es cierre
                        estado_actual = 0
                        if len(self.token) == conteo+1:  # para saber si estoy en la ultima linea
                            # print("llego")
                            return True
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \"-->\""))
                        return False
                case 7:
                    if token.tipo == "9":  # si es punto
                        estado_actual = 9
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \".\""))
                        return False
                case 8:
                    if token.tipo == "6":  # si es ;
                        estado_actual = 2
                        self.crearEtiqueta(controlTemporal, idTemporal)
                        controlTemporal = ""
                        idTemporal = ""
                    else:
                        self.errores.append(
                            Errores("Sintactico", token.fila, token.columna, token.lexema, "Falta \";\""))
                        return False
                case 9:
                    if token.tipo in self.metodo:  # si es metodo
                        metodoPropiedad = token
                        estado_actual = 10
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "El metodo no se reconoce o es invalido"))
                        return False
                case 10:
                    if token.tipo == "7":  # si es parentesis
                        estado_actual = 11
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \"(\""))
                        return False
                case 11:
                    if token.tipo in self.parametro:  # si es un parametro
                        parametroMetodo.append(token.lexema)
                        estado_actual = 12
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "No se esperaba ese token"))
                        return False
                case 12:
                    if token.tipo == "12":  # si es coma
                        estado_actual = 11
                    elif token.tipo == "8":  # si es parentesis
                        estado_actual = 13
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \")\""))
                        return False
                case 13:
                    if token.tipo == "6":  # si es ;
                        estado_actual = 3
                        self.agregarAtributo(
                            metodoPropiedad, idpropiedad, parametroMetodo)
                        parametroMetodo = []
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \";\""))
                        return False
                case 14:
                    if token.tipo == "9":  # si es punto
                        estado_actual = 16
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \".\""))
                        return False
                case 15:
                    if token.tipo == "9":  # si es punto
                        estado_actual = 26
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \".\""))
                        return False
                case 16:
                    if token.tipo == "setposicion":
                        metodoColocacion = "1"
                        estado_actual = 17
                    elif token.tipo == "add":
                        metodoColocacion = "2"
                        estado_actual = 18
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "El metodo es invalido o no lo es"))
                        return False
                case 18:
                    if token.tipo == "7":  # si es parentesis para add
                        estado_actual = 24
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \"(\""))
                        return False
                case 17:
                    if token.tipo == "7":  # si es parentesis
                        estado_actual = 19
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \"(\""))
                        return False
                case 19:
                    if token.tipo == "10":  # si es numero
                        parametroColo.append(token.lexema)
                        estado_actual = 20
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba un numero"))
                        return False
                case 20:
                    if token.tipo == "12":  # si es coma
                        estado_actual = 21
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Falta parametros o Se esperaba \",\" "))
                        return False
                case 21:
                    if token.tipo == "10":  # si es numero
                        parametroColo.append(token.lexema)
                        estado_actual = 22
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba un numero"))
                        return False
                case 22:
                    if token.tipo == "8":  # si es parentesis
                        estado_actual = 23
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \")\""))
                        return False
                case 23:
                    if token.tipo == "6":  # si es ;
                        estado_actual = 4
                        self.agregarColocacion(
                            metodoColocacion, idColocacion, parametroColo)
                        parametroColo = []
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \";\""))
                        return False
                case 24:
                    if token.tipo == "2":  # si es identificador
                        parametroColo.append(token.lexema)
                        estado_actual = 25
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba un identificador"))
                        return False
                case 25:
                    if token.tipo == "8":  # si es parentesis
                        estado_actual = 23
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "Se esperaba \")\""))
                        return False
                case 26:
                    if token.tipo == "add":
                        metodoColocacion = "2"
                        estado_actual = 18
                    else:
                        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "El metodo es invalido"))
                        return False
            conteo += 1
        self.errores.append(Errores(
                            "Sintactico", token.fila, token.columna, token.lexema, "No se esperaba \"" + token.lexema+"\""))
        #print(token.lexema + "   " + str(estado_actual) + " asdf")
        return False

    def agregarAtributo(self, metodo, id, parametros):
        existe = False
        conteo = 0
        posicionId = 0
        for iden in self.etiquetas:
            if iden.id == id:
                posicionId = conteo
                existe = True
            conteo += 1
        if existe == False:
            # agregar el id a errores de que no existe
            return False
        try:
            match(metodo.lexema.lower()):
                case "setcolorletra":
                    if len(parametros) == 3:
                        self.etiquetas[posicionId].colorletra = f"rgb({parametros[0]},{parametros[1]},{parametros[2]})"
                    # agregar error de que los parametros no son correctos
                case "settexto":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].texto = f"{parametros[0]}"
                case "setalineacion":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].alineacion = f"{parametros[0]}"
                case "setcolorfondo":
                    if len(parametros) == 3:
                        self.etiquetas[posicionId].colorFondo = f"rgb({parametros[0]},{parametros[1]},{parametros[2]})"
                case "setmarcada":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].marcado = f"{parametros[0]}"
                case "setgrupo":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].group = f"{parametros[0]}"
                case "setancho":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].x = f"{parametros[0]}"
                case "setalto":
                    if len(parametros) == 1:
                        self.etiquetas[posicionId].y = f"{parametros[0]}"
        except:
            self.errores.append(Errores(
                "Sintactico", metodo.fila, metodo.columna, metodo.lexema, "El metodo (\"" + metodo.lexema+"\") no se aplica al identificador \""+id+"\""))

    def agregarColocacion(self, metodo, id, parametros):
        match(metodo):
            case "1":  # setposicion
                if id == "this":
                    return False
                existe = False
                conteo = 0
                posicionId = 0
                for iden in self.etiquetas:
                    if iden.id == id:
                        posicionId = conteo
                        existe = True
                    conteo += 1
                if existe == False:
                    # agregar el id a errores de que no existe
                    return False
                if len(parametros) == 2:
                    self.etiquetas[posicionId].posicionx = f"{parametros[0]}"
                    self.etiquetas[posicionId].posiciony = f"{parametros[1]}"
                    return True
                # agregar error
            case "2":  # añadir
                if len(parametros) == 1:
                    existe = False
                    conteo = 0
                    posicionAG = 0
                    for iden in self.etiquetas:
                        if iden.id == parametros[0]:
                            posicionAG = conteo
                            existe = True
                        conteo += 1
                    if existe == False:
                        # agregar el id a errores de que no existe
                        return False
                    if id == "this":
                        self.cuerpoPagina.controles.append(
                            self.etiquetas[posicionAG])
                    else:
                        existe = False
                        conteo = 0
                        posicionId = 0
                        for iden in self.etiquetas:
                            if iden.id == id:
                                posicionId = conteo
                                existe = True
                            conteo += 1
                        if existe == False:
                            # agregar el id a errores de que no existe
                            return False
                        self.etiquetas[posicionId].controles.append(
                            self.etiquetas[posicionAG])
                        return True
