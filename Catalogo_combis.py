import tkinter as tk
from tkinter import ttk
import sqlite3

def centrar_ventana(ventana, ancho=600, alto=400):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"+{x}+{y}")

def conectar_combis_db():
    conn = sqlite3.connect("combis.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS combis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rutas TEXT,
            horarios TEXT,
            placas TEXT,
            modelo TEXT,
            marca TEXT,
            asientos INTEGER,
            imagen_path TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def obtener_rutas():
    conn, cursor = conectar_combis_db()
    cursor.execute("SELECT DISTINCT rutas FROM combis")
    rutas = [ruta[0] for ruta in cursor.fetchall()]
    conn.close()
    return rutas

def abrir_catalogo():
    ventana = tk.Toplevel()
    ventana.title("Catálogo de Combis")
    ventana.geometry("600x400")

    ventana.configure(bg="#2C2F33")
    centrar_ventana(ventana)

    btn_atras = tk.Button(ventana, text="Atrás", command=ventana.destroy, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
    btn_atras.pack(pady=10, padx=10, anchor="nw")

    titulo = tk.Label(ventana, text="CATÁLOGO", font=("Arial", 16, "bold"), fg="white", bg="#2C2F33")
    titulo.pack(pady=10)

    frame_busqueda = tk.Frame(ventana, bg="#2C2F33")
    frame_busqueda.pack(pady=10)

    label_ruta = tk.Label(frame_busqueda, text="SELECCIONE RUTA:", fg="white", bg="#2C2F33")
    label_ruta.grid(row=0, column=0, padx=5)

    rutas = obtener_rutas() # Obtenemos las rutas de la base de datos
    combo_rutas = ttk.Combobox(frame_busqueda, values=rutas, state="readonly", background="#99AAB5", foreground="black")
    combo_rutas.grid(row=0, column=1, padx=5)
    combo_rutas.current(0)

    frame_tabla = tk.Frame(ventana, bg="#2C2F33")
    frame_tabla.pack(pady=10)

    columns = ("Combi", "Hora de salida", "Hora de llegada")
    tabla = ttk.Treeview(frame_tabla, columns=columns, show="headings")

    tabla.heading("Combi", text="Combi")
    tabla.heading("Hora de salida", text="Hora de Salida")
    tabla.heading("Hora de llegada", text="Hora de Llegada")

    tabla.column("Combi", width=100, anchor="center")
    tabla.column("Hora de salida", width=150, anchor="center")
    tabla.column("Hora de llegada", width=150, anchor="center")

    tabla.pack()

    def buscar():
        ruta_seleccionada = combo_rutas.get()

        for row in tabla.get_children():
            tabla.delete(row)

        conn, cursor = conectar_combis_db()
        cursor.execute("SELECT nombre, horarios FROM combis WHERE rutas = ?", (ruta_seleccionada,))
        combis = cursor.fetchall()
        conn.close()

        if combis:
            for combi, horarios in combis:
                horarios_lista = horarios.split(",") # Suponiendo que los horarios están separados por comas
                if len(horarios_lista) >= 2:
                    hora_salida = horarios_lista[0]
                    hora_llegada = horarios_lista[1]
                    tabla.insert("", "end", values=(combi, hora_salida, hora_llegada))

    btn_buscar = tk.Button(frame_busqueda, text="Consultar", command=buscar, bg="#43B581", fg="white", font=("Arial", 10, "bold"))
    btn_buscar.grid(row=0, column=2, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Catálogo de Combis")
    root.geometry("400x300")
    root.configure(bg="#2C2F33")

    btn_abrir_catalogo = tk.Button(root, text="Abrir Catálogo", command=abrir_catalogo, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
    btn_abrir_catalogo.pack(pady=20)

    root.mainloop()