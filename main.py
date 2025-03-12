import tkinter as tk
from tkinter import messagebox, Toplevel
from Agregar_combi import CombiApp
from Catalogo_combis import abrir_catalogo
from Reservar_Asientos import ReservaAsientosApp
from Editar_Combi import EditarCombiApp
from Administrar_Usuario import administrar_usuario

def centrar_ventana(ventana, ancho=500, alto=600):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"+{x}+{y}")

def abrir_agregar_combi():
    ventana = Toplevel(root)
    app = CombiApp(ventana)

def editar_combi():
    ventana = Toplevel(root)
    app = EditarCombiApp(ventana)

def abrir_reservar_asientos():
    ventana_reserva = Toplevel(root)
    app_reserva = ReservaAsientosApp(ventana_reserva)

def abrir_administrar_usuario():
    administrar_usuario()

def salir():
    root.quit()

# Crear ventana principal
root = tk.Tk()
root.title("Sistema de Combis")
root.configure(bg="#2C2F33") #color de fondo

centrar_ventana(root)

frame = tk.Frame(root, bg="#2C2F33", padx=40, pady=40) #color de fondo y padding
frame.pack(pady=10)

btn_agregar_combi = tk.Button(frame, text="Agregar combi", command=abrir_agregar_combi, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_agregar_combi.grid(row=0, column=0, padx=5, pady=5)

btn_editar_combi = tk.Button(frame, text="Editar combi", command=editar_combi, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_editar_combi.grid(row=1, column=0, padx=5, pady=5)

btn_reserva_asientos = tk.Button(frame, text="Registrar viaje", command=abrir_reservar_asientos, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_reserva_asientos.grid(row=0, column=2, padx=5, pady=5)

btn_catalogo = tk.Button(frame, text="Catálogo", command=abrir_catalogo, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_catalogo.grid(row=0, column=3, padx=5, pady=5)

btn_administrar_usuario = tk.Button(frame, text="Administrar usuario", command=abrir_administrar_usuario, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_administrar_usuario.grid(row=0, column=4, padx=5, pady=5)

btn_salir = tk.Button(root, text="Salir", command=salir, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
btn_salir.pack(pady=10)

mensaje = tk.Label(root, text="BIENVENIDO\nAgregue su primera combi", font=("Arial", 12), fg="white", bg="#2C2F33") #color de texto y fondo
mensaje.pack(pady=20)

root.mainloop()
