from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter.colorchooser import askcolor
from tkinter import ttk
import re
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
import random

def conexion():
    con = sqlite3.connect("entrega_final.db")
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS participantes
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo VARCHAR(30) NOT NULL,
            nacionalidad VARCHAR(15) NOT NULL,
            estadio VARCHAR(20) NOT NULL)
             """
    cursor.execute(sql)
    con.commit()

try:
    conexion()
    crear_tabla()
except:
    print("Hay un error")

def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM participantes ORDER BY id DESC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
    con.close()

def alta(eq1, eq2, eq3, tree):
    patron = "^[A-Za-záéíóúñÑ0-9 ]*$"
    if re.match(patron, eq1) and re.match(patron, eq2) and re.match(patron, eq3):
        con = conexion()
        cursor = con.cursor()
        sql = "INSERT INTO participantes (equipo, nacionalidad, estadio) VALUES (?, ?, ?)"
        cursor.execute("SELECT equipo FROM participantes")
        equipos_existentes = [fila[0] for fila in cursor.fetchall()]
        if eq1 in equipos_existentes:
            showerror("Error", "El equipo ya existe en la base de datos.")
        else:
            sql = "INSERT INTO participantes (equipo, nacionalidad, estadio) VALUES (?, ?, ?)"
            cursor.execute(sql, (eq1, eq2, eq3))
            con.commit()
            con.close()
            actualizar_treeview(tree)
    else:
        showerror("Error", "Los campos deben contener solo letras y espacios.")

def borrar(tree):
    valor = tree.selection()
    if valor:
        item = tree.item(valor)
        mi_id = item['text']
        con = conexion()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM participantes WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        showinfo("Cambios Realizados", "Equipo borrado exitosamente.")
        con.close()
    else:
        showerror("Error", "Selecciona un equipo para eliminar.")

def borrar_todo(tree):
    con = conexion()
    cursor = con.cursor() 
    sql = "DELETE FROM participantes"
    cursor.execute(sql)
    con.commit()         
    records = tree.get_children()
    for element in records:
        tree.delete(element)    
    showinfo("Borrado Exitoso", "Se han borrado todos los registros.")
    con.close()

def modificar(tree):
    valor = tree.selection()
    if not valor:
        showerror("Error", "Selecciona un equipo para modificar.")
        return
    item = tree.item(valor)
    item_id = item['text']
    nuevo_nombre = eq1.get()
    nueva_nacionalidad = eq2.get()
    nuevo_estadio = eq3.get()
    con = conexion()
    cursor = con.cursor()
    sql = "UPDATE participantes SET equipo=?, nacionalidad=?, estadio=? WHERE id=?"
    cursor.execute(sql, (nuevo_nombre, nueva_nacionalidad, nuevo_estadio, item_id))
    con.commit()
    con.close()
    eq1.set('')
    eq2.set('')
    eq3.set('')
    actualizar_treeview(tree)
    showinfo("Cambios Realizados", "Los cambios se han guardado exitosamente.")
    con.close()

def consulta(tree):
    for item in tree.get_children():
        values = tree.item(item, 'values')
        print("ID:", item) 
        print("Nombre:", values[0])  
        print("Nacionalidad:", values[1])  
        print("Estadio:", values[2]) 
        print("----")  

equipos = ["Equipo A", "Equipo B", "Equipo C", "Equipo D", "Equipo E", "Equipo F", "Equipo G", "Equipo H"]

def simulacion(equipo1, equipo2):
    if len(equipo1) == 0 or len(equipo2) == 0:
        return "No hay suficientes equipos para simular un partido.", ""
    
    equipo_local = random.randint(0, 5)
    equipo_visitante = random.randint(0, 5)
    
    if equipo_visitante == equipo_local:
        penales_local = random.randint(0, 10)
        penales_visitante = random.randint(0, 10)
        
        if penales_local > penales_visitante:
            ganador = equipo1
            resultado = f"{equipo1} {equipo_local} - {equipo2} {equipo_visitante}, Ganador: {ganador}, por penales"
        elif penales_local < penales_visitante:
            ganador = equipo2
            resultado = f"{equipo1} {equipo_local} - {equipo2} {equipo_visitante}, Ganador: {ganador}, por penales"
        else:
            ganador = "Sin ganador"
            resultado = f"{equipo1} {equipo_local} - {equipo2} {equipo_visitante}, Empate, se define por penales"
    else:
        if equipo_local > equipo_visitante:
            ganador = equipo1
        elif equipo_local < equipo_visitante:
            ganador = equipo2
        else:
            ganador = "Sin ganador"
    
    resultado = f"{equipo1} {equipo_local} - {equipo2} {equipo_visitante}, Ganador: {ganador}"
    if(equipo1 == equipo2):
        resultado = f"{equipo1} {equipo_local} - {equipo2} {equipo_visitante}, Sin ganador, se define por penales"
    return resultado, ganador

def simular_torneo():
    con = conexion()
    cursor = con.cursor()
    sql = "SELECT equipo FROM participantes"
    cursor.execute(sql)
    equipos = [fila[0] for fila in cursor.fetchall()]
    con.close()
    
    if len(equipos) != 8:
        return "Debe haber exactamente 8 equipos en la base de datos para simular el torneo."
    
    while len(equipos) > 1:
        ronda = []
        for i in range(0, len(equipos), 2):
            equipo1, equipo2 = equipos[i], equipos[i+1]
            resultado, ganador = simulacion(equipo1, equipo2)
            print(resultado)
            ronda.append(ganador)
        equipos = ronda
    
    campeon = equipos[0]
    resultado_final = f"El ganador del torneo es {campeon}."
    return resultado_final

def comenzar_torneo():
    resultado = simular_torneo()
    if resultado.startswith("Error"):
        showerror("Error", resultado)
    else:
        showinfo("Resultado del torneo", resultado)
        print(resultado)

def cambiocolor():
    seleccion = askcolor(color='#06A267', title="Eleccion de color")
    if seleccion[1]:
        frame_input.configure(bg=seleccion[1])
        frame_treeview.configure(bg=seleccion[1])
        frame_botones.configure(bg=seleccion[1])
        frame_color.configure(bg=seleccion[1])
        root.configure(bg=seleccion[1])
        imagen_label.configure(bg=seleccion[1])
        equipo1.configure(bg=seleccion[1])
        equipo2.configure(bg=seleccion[1])
        equipo3.configure(bg=seleccion[1])

def cargar_datos_iniciales(tree):
    con = conexion()
    cursor = con.cursor()
    sql = "SELECT * FROM participantes ORDER BY id DESC"
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))
    con.close()

root = Tk()
root.title("Simulador de Torneos")
root.configure(bg="#F0F0F0")

frame_titulo = Frame(root, bg="#06A267", padx=10, pady=10)
frame_titulo.grid(row=0, column=0, columnspan=3, sticky="nsew")

frame_subtitulo = Frame (root, bg="#06A267", padx=10, pady=10)
frame_subtitulo.grid(row=1, column=0, columnspan=3, sticky="nsew")

frame_input = Frame(root, padx=10, pady=20, borderwidth=3)
frame_input.grid(row=2, column=0, rowspan=3, sticky="nsew")

frame_treeview = Frame(root, padx=10, pady=10)
frame_treeview.grid(row=3, column=1, rowspan=3, sticky="nsew")

frame_botones = Frame(root, padx=10, pady=10)
frame_botones.grid(row=0, column=2, rowspan=4, sticky="nsew")

frame_color = Frame(root, padx=10, pady=10)
frame_color.grid(row=5, column=0, columnspan=2, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

imagen = Image.open("torneo.png")
achicada = imagen.resize((120,120))
foto = ImageTk.PhotoImage(achicada)

imagen_label = Label(root, image=foto, bg="#F0F0F0")
imagen_label.grid(row=4, column=0)

titulo = Label(frame_titulo, text="NUEVO TORNEO", bg="#06A267", fg="#FFFFFF", font=("Helvetica", 16))
titulo.grid(row=0, column=0, columnspan=2, sticky="nsew")
instruccion = Label(frame_subtitulo, text="Ingrese 8 equipos para comenzar el torneo", bg="#06A267", fg="#FFFFFF", font=("Helvetica", 12))
instruccion.grid(row=1, column=0, columnspan=2, sticky="nsew")

equipo1 = Label(frame_input, text="Nombre del equipo: ", bg="#F0F0F0")
equipo1.grid(row=0, column=0, sticky="w")

equipo2 = Label(frame_input, text="Pais de origen: ", bg="#F0F0F0")
equipo2.grid(row=1, column=0, sticky="w")

equipo3 = Label(frame_input, text="Estadio: " , bg="#F0F0F0")
equipo3.grid(row= 2, column=0, sticky="W")

eq1, eq2, eq3= StringVar(), StringVar(), StringVar()
w_ancho = 20

entrada1 = Entry(frame_input, textvariable=eq1, width=w_ancho)
entrada1.grid(row=0, column=1)
entrada2 = Entry(frame_input, textvariable=eq2, width=w_ancho)
entrada2.grid(row=1, column=1)
entrada3 = Entry(frame_input, textvariable=eq3, width=w_ancho)
entrada3.grid(row=2, column=1)

style = ttk.Style()
style.configure("Treeview.Heading", background="white", foreground="black")

tree = ttk.Treeview(frame_treeview)
cargar_datos_iniciales(tree)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Nombre")
tree.heading("col2", text="Nacionalidad")
tree.heading("col3", text="Estadio")
tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

boton_alta = Button(frame_botones, text="Agregar Equipo", command=lambda: alta(entrada1.get(), entrada2.get(), entrada3.get(), tree), width=20, borderwidth=3)
boton_alta.grid(row=0, column=0, pady=5)

boton_borrar = Button(frame_botones, text="Borrar equipo", command=lambda: borrar(tree), width=20, borderwidth=3)
boton_borrar.grid(row=1, column=0, pady=5)

boton_borrartodo = Button(frame_botones, text="Borrar todos", command=lambda: borrar_todo(tree), width=20, borderwidth=3)
boton_borrartodo.grid(row=2, column=0, pady=5)

boton_consulta = Button(frame_botones, text="Consultar participantes", command=lambda: consulta(tree), width=20, borderwidth=3)
boton_consulta.grid(row=3, column=0, pady=5)

boton_modificar = Button(frame_botones, text="Modificar equipo", command=lambda: modificar(tree), width=20, borderwidth=3)
boton_modificar.grid(row=4, column=0, pady=5)

boton_simulacion = Button(frame_botones, text="Comenzar torneo", command=comenzar_torneo, width=20, borderwidth=3)
boton_simulacion.grid(row=5, column=0, pady=5)

boton_salida = Button(frame_botones, text="Salir", command=root.quit, width=20, borderwidth=3)
boton_salida.grid(row=6, column=0, pady=5)

boton_colores = Button(frame_color, text="Cambiar color", command=lambda: cambiocolor(), width=20, borderwidth=3)
boton_colores.grid(row=7, column=0)

root.mainloop()
