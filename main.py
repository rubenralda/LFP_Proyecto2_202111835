import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from analizador import *
import webbrowser


class Principal(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, height=650, width=1020)
        self.master = master
        self.tokens = []
        self.direccionGlobal = ""
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Editor de código")
        self.label.place(x=160, y=5)
        self.textBox = tk.Text(self, height=27, width=105)
        self.textBox.place(x=160, y=30)
        # menu archivo
        self.label2 = tk.Label(self, text="Menú de archivo")
        self.label2.place(x=20, y=5)
        self.buttonNuevo = tk.Button(
            self, text="Nuevo", command=self.nuevoArchivo)
        self.buttonNuevo.place(x=20, y=30)
        self.buttonAbrir = tk.Button(
            self, text="Abrir", command=self.abrirArchivo)
        self.buttonAbrir.place(x=20, y=70)
        self.buttonGuardar = tk.Button(
            self, text="Guardar", command=self.guardarArchivo)
        self.buttonGuardar.place(x=20, y=110)
        self.buttonGuardarComo = tk.Button(
            self, text="Guardar como...", command=self.guardarComo)
        self.buttonGuardarComo.place(x=20, y=150)
        self.buttonSalir = tk.Button(
            self, text="Salir", command=self.master.destroy)
        self.buttonSalir.place(x=20, y=190)
        # menu analisis
        self.label2 = tk.Label(self, text="Menú de análisis")
        self.label2.place(x=20, y=230)
        self.buttonAnalizar = tk.Button(
            self, text="Generar página web", command=self.analizar)
        self.buttonAnalizar.place(x=20, y=260)
        # menu tokens
        self.buttonToken = tk.Button(
            self, text="Mostrar Tokens", command=self.mostrarTokens)
        self.buttonToken.place(x=20, y=300)
        # tabla errores
        self.tablaErrores = ttk.Treeview(columns=(
            "#1", "#2", "#3", "#4", "#5"))
        self.tablaErrores.column("#0", width=50, anchor=tk.CENTER)
        self.tablaErrores.heading("#0", text="No.")
        self.tablaErrores.column("#1", anchor=tk.CENTER, width=100)
        self.tablaErrores.heading("#1", text="Tipo")
        self.tablaErrores.column("#2", anchor=tk.CENTER, width=50)
        self.tablaErrores.heading("#2", text="Línea")
        self.tablaErrores.column("#3", anchor=tk.CENTER, width=100)
        self.tablaErrores.heading("#3", text="Posición del error")
        self.tablaErrores.column("#4", anchor=tk.CENTER, width=170)
        self.tablaErrores.heading("#4", text="Token")
        self.tablaErrores.column("#5", anchor=tk.CENTER, width=300)
        self.tablaErrores.heading("#5", text="Descripción")
        self.tablaErrores.place(x=10, y=480, height=150, width=1000)

    def nuevoArchivo(self):
        if self.direccionGlobal != "":#si hay un archivo cargado
            self.guardarComo()
        self.textBox.delete(1.0, tk.END)

    def abrirArchivo(self):
        filetypes = (
            ('text files', '*.gpw'),
            ('All files', '*.*')
        )
        try:
            direccion = filedialog.askopenfilename(
                initialdir="/", title="Escoge el Archivo", filetypes=filetypes)
            if direccion != "":
                self.direccionGlobal = direccion
                file = open(self.direccionGlobal, mode="r", encoding="utf-8")
                self.textBox.delete(1.0, tk.END)
                for linea in file:
                    self.textBox.insert(tk.END, linea)
                file.close()
        except:
            messagebox.showerror("Error", "Error al cargar el archivo")

    def guardarArchivo(self):
        self.guardar("w", self.direccionGlobal)

    def guardarComo(self):
        filetypes = (
            ('text files', '*.gpw'),
            ('All files', '*.*')
        )
        direccionNueva = filedialog.asksaveasfilename(
            initialdir="/", title="Escoge la carpeta", filetypes=filetypes, defaultextension="gpw")
        if direccionNueva != "":
            self.direccionGlobal = direccionNueva
            self.guardar("x", direccionNueva)

    def guardar(self, mode="", direccion=""):
        try:
            file = open(direccion, mode=mode, encoding="utf-8")
            file.write(self.textBox.get("1.0", tk.END))
            file.close()
            messagebox.showinfo("Información", "Se ha editado correctamente")
        except:
            messagebox.showwarning("Cuidado", "No se pudo guardar el archivo")

    def analizar(self):
        if self.direccionGlobal != "":  # si existe un archivo
            body = ""
            css = ""
            cabeza = ""
            auto = Automatas(
                open(self.direccionGlobal, "r", encoding="utf-8").read())
            auto.lexico()
            self.tokens = auto.token
            if auto.sintactico() == True and auto.errores == []:  # verifica si todo ocurrio sin problemas
                html = open(self.direccionGlobal[0:len(self.direccionGlobal)-3]+"html", "w", encoding="utf-8")
                cabeza = f"""<!DOCTYPE html>
                            <html lang="en">
                            <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <link rel="stylesheet" href="{self.direccionGlobal[0:len(self.direccionGlobal)-3]+"css"}">
                            <title>Document</title><body>"""
                for cuerpo in auto.cuerpoPagina.controles:
                    body += cuerpo.crearHtml()
                body += """</body></html>"""
                html.write(cabeza + body)
                html.close()
                archivoCss = open(self.direccionGlobal[0:len(self.direccionGlobal)-3]+"css", "w", encoding="utf-8")
                for control in auto.etiquetas:
                    css += control.crearCss()
                archivoCss.write(css)
                archivoCss.close()
                webbrowser.open(self.direccionGlobal[0:len(self.direccionGlobal)-3]+"html")
            else:  # si no se cumple muestra los errores
                self.tablaErrores.delete(*self.tablaErrores.get_children())
                contador = 1
                for error in auto.errores:
                    self.tablaErrores.insert("", tk.END, text=str(contador),
                                             values=(error.tipo, str(error.fila), str(error.columna), error.error, error.descripcion))
                    contador += 1
                messagebox.showerror("Error", "El archivo no se pudo crear")
        else:
            messagebox.showwarning("Cuidado", "Cargue un archivo primero")

    def mostrarTokens(self):
        if self.tokens == []:
            messagebox.showwarning("Cuidado", "No hay tokens que mostrar")
            return
        self.listar = tk.Tk()
        self.listar.resizable(False, False)
        self.listar.title("Listado de Tokens")
        self.listar.geometry("980x640+"+str((self.listar.winfo_screenwidth()-980) //
                             2)+"+"+str((self.listar.winfo_screenheight()-600)//2))
        self.listar.attributes("-topmost", True)
        # conf Frame
        self.marco4 = tk.Frame(self.listar, border=10, relief="sunken")
        self.marco4.place(x=20, y=20, width=942, height=560)
        # conf tabla y boton Regresar
        self.tabla = ttk.Treeview(self.marco4, columns=(
            "#1", "#2", "#3", "#4", "#5", "#6"))
        self.tabla.column("#0", width=100, anchor=tk.CENTER)
        self.tabla.heading("#0", text="CORRELATIVO")
        self.tabla.column("#1", anchor=tk.CENTER, width=350)
        self.tabla.heading("#1", text="TOKEN")
        self.tabla.column("#2", anchor=tk.CENTER, width=250)
        self.tabla.heading("#2", text="LEXEMA")
        self.bregresar_gestion = tk.Button(
            self.listar, text="Salir", command=self.listar.destroy)
        self.bregresar_gestion.place(x=440, y=595, width=100, height=30)
        contador = 1
        for token in self.tokens:
            self.tabla.insert("", tk.END, text=str(contador),
                              values=(token.tipo, token.lexema))
            contador += 1
        self.tabla.place(x=0, y=0, height=540)
        # Inicia la ventana para el listado de cursos
        self.listar.mainloop()


root = tk.Tk()
root.title("Menu")
app = Principal(master=root)
app.mainloop()
