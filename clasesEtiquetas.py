class Etiqueta:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.x = "100"
        self.y = "25"
        self.posicionx = "0"
        self.posiciony = "0"
        self.colorletra = ""
        self.colorFondo = ""

    def crearHtml(self):
        html = f"<label id=\"{self.id}\"> {self.texto[1:len(self.texto)-1]} </label>"
        return html

    def crearCss(self):
        colorLetra = ""
        if self.colorletra != "":
            colorLetra = "color: " + self.colorletra+";"
        colorFondo = ""
        if self.colorFondo != "":
            colorFondo = "background-color: " + self.colorFondo + ";"
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;"+ posicionx+ posiciony +colorLetra+\
            colorFondo + \
            "width: "+self.x+"px; height: "+self.y+"px;}"
        return css


class Boton:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.alineacion = "izquierdo"
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        alinear = {"centro":"center","izquierdo":"left","derecho":"right"}
        html = f"<input type=\"submit\" id=\"{self.id}\" value={self.texto} style=\"text-align: {alinear[self.alineacion.lower()]}\"/>"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;" + posicionx + posiciony +" width: 100px; height: 25px;}"
        return css


class Check:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.marcado = "False"
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        marcado = ""
        if self.marcado.lower() == "true":
            marcado = "checked"
        html = f"<input type=\"checkbox\" id=\"{self.id}\" {marcado} />{self.texto[1:len(self.texto)-1]}"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;" + posicionx+ posiciony+" width: 100px; height: 25px;}"
        return css


class RadioBoton:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.marcado = "False"
        self.group = id
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        marcado = ""
        if self.marcado.lower() == "true":
            marcado = "checked"
        html = f"<input type=\"radio\" name=\"{self.group}\" id=\"{self.id}\" {marcado} />{self.texto[1:len(self.texto)-1]}"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;" + posicionx+ posiciony+" width: 100px; height: 25px;}"
        return css


class Texto:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.alineacion = "izquierdo"
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        alinear = {"centro":"center","izquierdo":"left","derecho":"right"}
        html = f"<input type=\"text\" id=\"{self.id}\" value={self.texto} style=\"text-align: {alinear[self.alineacion.lower()]}\"/>"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;" + posicionx + posiciony+"width: 100px; height: 25px;}"
        return css


class AreaTexto:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        html = f"<TEXTAREA id=\"{self.id}\">{self.texto[1:len(self.texto)-1]}</TEXTAREA> "
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;"+ posicionx+ posiciony+"width: 150px; height: 150px;}"
        return css


class Clave:
    def __init__(self, id=""):
        self.id = id
        self.texto = "\"\""
        self.alineacion = "izquierdo"
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        alinear = {"centro":"center","izquierdo":"left","derecho":"right"}
        html = f"<input type=\"password\" id=\"{self.id}\" value={self.texto} style=\"text-align: {alinear[self.alineacion.lower()]}\"/>"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        css = "#"+self.id+"{position: absolute;" + posicionx+ posiciony+"width: 100px; height: 25px;}"
        return css


class Contenedor:
    def __init__(self, id=""):
        self.id = id
        self.x = "100"
        self.y = "100"
        self.colorFondo = ""
        self.controles = []
        self.posicionx = "0"
        self.posiciony = "0"

    def crearHtml(self):
        html = f"<div id=\"{self.id}\">"
        for control in self.controles:
            html += control.crearHtml()
        html += "</div>"
        return html

    def crearCss(self):
        posicionx = ""
        if self.posicionx != "0":
            posicionx =  "left: " + self.posicionx + "px;"
        posiciony = ""
        if self.posiciony != "0":
            posiciony = "top: " + self.posiciony + "px;"
        colorFondo = ""
        if self.colorFondo != "":
            colorFondo = "background-color: " + self.colorFondo + ";"
        css = "#"+self.id+"{position: absolute;" + posicionx+ posiciony+ \
                colorFondo + "width: "+self.x+"px; height: "+self.y+"px;}"
        return css


class This:
    def __init__(self):
        self.controles = []
    