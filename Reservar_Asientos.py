import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

def conectar_reservas_db():
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            combi TEXT NOT NULL,
            ruta TEXT NOT NULL,
            horario TEXT NOT NULL,
            asiento INTEGER NOT NULL
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

def obtener_horarios_por_ruta(ruta):
    conn, cursor = conectar_combis_db()
    cursor.execute("SELECT DISTINCT horarios FROM combis WHERE rutas = ?", (ruta,))
    horarios = [horario[0] for horario in cursor.fetchall()]
    conn.close()
    return horarios

def obtener_combis_por_ruta_y_horario(ruta, horario):
    conn, cursor = conectar_combis_db()
    cursor.execute("SELECT nombre FROM combis WHERE rutas = ? AND horarios = ?", (ruta, horario))
    combis = [combi[0] for combi in cursor.fetchall()]
    conn.close()
    return combis

def obtener_asientos_combi(combi_nombre):
    conn, cursor = conectar_combis_db()
    cursor.execute("SELECT asientos FROM combis WHERE nombre = ?", (combi_nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0

class ReservaAsientosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reservar Asiento")
        self.root.geometry("800x450")
        self.root.configure(bg="#2C2F33")

        self.btn_atras = tk.Button(self.root, text="← Atrás", font=("Arial", 10, "bold"), bg="#7289DA", fg="white", command=self.root.destroy)
        self.btn_atras.place(x=10, y=10, width=60, height=30)

        self.entry_usuario = tk.Entry(self.root, font=("Arial", 12), bg="#99AAB5", fg="black")
        self.entry_usuario.place(x=300, y=10, width=200, height=30)
        self.entry_usuario.insert(0, "Agregar usuario")
        self.entry_usuario.bind("<FocusIn>", self.on_entry_click)
        self.entry_usuario.bind("<FocusOut>", self.on_focusout)

        self.ruta_label = tk.Label(self.root, text="Seleccionar Ruta:", font=("Arial", 10), bg="#2C2F33", fg="white")
        self.ruta_label.place(x=50, y=70)
        self.ruta_combobox = ttk.Combobox(self.root, values=obtener_rutas(), state="readonly")
        self.ruta_combobox.place(x=200, y=70, width=150)
        self.ruta_combobox.bind("<<ComboboxSelected>>", self.cargar_horarios)

        self.horario_label = tk.Label(self.root, text="Seleccionar Horario:", font=("Arial", 10), bg="#2C2F33", fg="white")
        self.horario_label.place(x=50, y=110)
        self.horario_combobox = ttk.Combobox(self.root, state="readonly")
        self.horario_combobox.place(x=200, y=110, width=150)
        self.horario_combobox.bind("<<ComboboxSelected>>", self.cargar_combis)

        self.combi_label = tk.Label(self.root, text="Seleccionar Combi:", font=("Arial", 10), bg="#2C2F33", fg="white")
        self.combi_label.place(x=50, y=150)
        self.combi_combobox = ttk.Combobox(self.root, state="readonly")
        self.combi_combobox.place(x=200, y=150, width=150)
        self.combi_combobox.bind("<<ComboboxSelected>>", self.cargar_asientos)

        self.asiento_label = tk.Label(self.root, text="Seleccionar Asiento:", font=("Arial", 10), bg="#2C2F33", fg="white")
        self.asiento_label.place(x=50, y=190)
        self.asiento_combobox = ttk.Combobox(self.root, state="readonly")
        self.asiento_combobox.place(x=200, y=190, width=150)

        self.btn_registrar = tk.Button(self.root, text="Registrar", font=("Arial", 12, "bold"), bg="#43B581", fg="white", command=self.registrar_reserva)
        self.btn_registrar.place(x=120, y=250, width=150, height=40)

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="#2C2F33", highlightthickness=1, highlightbackground="white")
        self.canvas.place(x=450, y=50)

        self.leyenda_frame = tk.Frame(self.root, bg="#2C2F33")
        self.leyenda_frame.place(x=450, y=370)
        colores = {"Disponible": "white", "Seleccionado": "orange", "Ocupado": "gray", "Deshabilitado": "darkgray"}
        for i, (estado, color) in enumerate(colores.items()):
            tk.Canvas(self.leyenda_frame, width=20, height=20, bg=color, highlightthickness=1).grid(row=i, column=0, padx=5, pady=2)
            tk.Label(self.leyenda_frame, text=estado, bg="#2C2F33", fg="white").grid(row=i, column=1, padx=5, pady=2)

    def on_entry_click(self, event):
        if self.entry_usuario.get() == "Agregar usuario":
            self.entry_usuario.delete(0, tk.END)

    def on_focusout(self, event):
        if not self.entry_usuario.get():
            self.entry_usuario.insert(0, "Agregar usuario")

    def cargar_horarios(self, event):
        ruta_seleccionada = self.ruta_combobox.get()
        horarios = obtener_horarios_por_ruta(ruta_seleccionada)
        self.horario_combobox["values"] = horarios if horarios else ["No disponible"]
        if horarios:
            self.horario_combobox.current(0)
            self.cargar_combis(event)
        else:
            self.combi_combobox["values"] = []
            self.asiento_combobox["values"] = []
            self.canvas.delete("all")

    def cargar_combis(self, event):
        ruta_seleccionada = self.ruta_combobox.get()
        horario_seleccionado = self.horario_combobox.get()
        combis = obtener_combis_por_ruta_y_combis = obtener_combis_por_ruta_y_horario(ruta_seleccionada, horario_seleccionado)
        self.combi_combobox["values"] = combis if combis else ["No disponible"]
        if combis:
            self.combi_combobox.current(0)
            self.cargar_asientos(event)
        else:
            self.asiento_combobox["values"] = []
            self.canvas.delete("all")

    def cargar_asientos(self, event):
        combi_seleccionada = self.combi_combobox.get()
        num_asientos = obtener_asientos_combi(combi_seleccionada)
        self.asiento_combobox["values"] = [str(i + 1) for i in range(num_asientos)]
        if num_asientos > 0:
            self.asiento_combobox.current(0)
            self.generar_asientos()
        else:
            self.canvas.delete("all")

    def generar_asientos(self):
        self.canvas.delete("all")
        combi_seleccionada = self.combi_combobox.get()
        num_asientos = obtener_asientos_combi(combi_seleccionada)
        for i in range(num_asientos):
            x, y = (i % 4) * 50 + 10, (i // 4) * 50 + 10
            self.canvas.create_rectangle(x, y, x + 40, y + 40, fill="white", outline="black")
            self.canvas.create_text(x + 20, y + 20, text=str(i + 1), font=("Arial", 10, "bold"))

    def registrar_reserva(self):
        usuario = self.entry_usuario.get()
        combi = self.combi_combobox.get()
        ruta = self.ruta_combobox.get()
        horario = self.horario_combobox.get()
        asiento = self.asiento_combobox.get()

        if usuario == "Agregar usuario" or not combi or not ruta or not horario or not asiento:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

        conn, cursor = conectar_reservas_db()
        cursor.execute("INSERT INTO reservas (usuario, combi, ruta, horario, asiento) VALUES (?, ?, ?, ?, ?)",
                       (usuario, combi, ruta, horario, asiento))
        conn.commit()
        conn.close()

        respuesta = messagebox.askyesno("Reserva Guardada", "¿Reserva guardada con éxito! ¿Desea realizar otra reserva?")
        if respuesta:
            self.limpiar_campos()
        else:
            self.root.destroy()

    def limpiar_campos(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_usuario.insert(0, "Agregar usuario")
        self.ruta_combobox.set("")
        self.horario_combobox.set("")
        self.combi_combobox.set("")
        self.asiento_combobox.set("")
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservaAsientosApp(root)
    root.mainloop() 
