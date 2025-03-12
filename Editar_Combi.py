import tkinter as tk
from tkinter import messagebox
import os
import sys
import sqlite3

def get_database_path(filename):
    """Obtiene la ruta correcta de la base de datos, ya sea en desarrollo o en .exe"""
    if getattr(sys, 'frozen', False):  # Si está congelado (.exe)
        base_path = sys._MEIPASS  # Carpeta temporal donde PyInstaller extrae archivos
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Carpeta normal
    return os.path.join(base_path, filename)

DB_PATH = get_database_path("combis.db")

def conectar_combis_db():
    conn = sqlite3.connect(DB_PATH)
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

def centrar_ventana(ventana, ancho=600, alto=400):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"+{x}+{y}")

class EditarCombiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editar Combis")
        self.root.configure(bg="#2C2F33")

        self.frame = tk.Frame(root, padx=20, pady=20, bg="#2C2F33")
        self.frame.pack()

        self.btn_atras = tk.Button(self.frame, text="← Atrás", width=20, bg="#7289DA", fg="white", font=("Arial", 10, "bold"),
                                    command=self.root.destroy)
        self.btn_atras.grid(row=0, column=0, sticky='w', pady=5)

        self.label_titulo = tk.Label(self.frame, text="Editar Combi", font=("Arial", 16, "bold"), fg="white", bg="#2C2F33")
        self.label_titulo.grid(row=0, column=1, columnspan=2)

        self.combis = self.cargar_combis()

        self.label_seleccionar = tk.Label(self.frame, text="Seleccionar combi:", fg="white", bg="#2C2F33")
        self.label_seleccionar.grid(row=1, column=0, pady=5)

        self.combi_var = tk.StringVar()
        self.combi_menu = tk.OptionMenu(self.frame, self.combi_var, *self.combis, command=self.cargar_datos_combi)
        self.combi_menu.grid(row=1, column=1, pady=5)

        self.entries = {}
        info_labels = ["Rutas", "Horarios", "Placas", "Modelo", "Marca"]

        for i, label in enumerate(info_labels):
            lbl = tk.Label(self.frame, text=label, width=20, fg="white", bg="#2C2F33")
            lbl.grid(row=2+i, column=0, pady=2)
            entry = tk.Entry(self.frame, width=22, bg="#99AAB5", fg="black")
            entry.grid(row=2+i, column=1, pady=2)
            self.entries[label] = entry

        self.btn_guardar = tk.Button(self.frame, text="Guardar cambios", width=22, bg="#43B581", fg="white", font=("Arial", 10, "bold"),
                                        command=self.guardar_cambios)
        self.btn_guardar.grid(row=8, column=0, columnspan=2, pady=10)

        if self.combis:
            self.combi_var.set(self.combis[0])
            self.cargar_datos_combi(self.combis[0])

        centrar_ventana(self.root)

    def cargar_combis(self):
        conn, cursor = conectar_combis_db()
        cursor.execute("SELECT nombre FROM combis")
        combis = [row[0] for row in cursor.fetchall()]
        conn.close()
        return combis

    def cargar_datos_combi(self, combi_nombre):
        conn, cursor = conectar_combis_db()
        cursor.execute("SELECT rutas, horarios, placas, modelo, marca FROM combis WHERE nombre = ?", (combi_nombre,))
        datos = cursor.fetchone()
        conn.close()

        if datos:
            rutas, horarios, placas, modelo, marca = datos
            self.entries["Rutas"].delete(0, tk.END)
            self.entries["Horarios"].delete(0, tk.END)
            self.entries["Placas"].delete(0, tk.END)
            self.entries["Modelo"].delete(0, tk.END)
            self.entries["Marca"].delete(0, tk.END)
            self.entries["Rutas"].insert(0, rutas)
            self.entries["Horarios"].insert(0, horarios)
            self.entries["Placas"].insert(0, placas)
            self.entries["Modelo"].insert(0, modelo)
            self.entries["Marca"].insert(0, marca)

    def guardar_cambios(self):
        nombre_combi = self.combi_var.get()
        if not nombre_combi:
            messagebox.showerror("Error", "Seleccione una combi para editar.")
            return

        nuevos_datos = {k: v.get() for k, v in self.entries.items()}

        conn, cursor = conectar_combis_db()
        cursor.execute("UPDATE combis SET rutas = ?, horarios = ?, placas = ?, modelo = ?, marca = ? WHERE nombre = ?",
                       (nuevos_datos["Rutas"], nuevos_datos["Horarios"], nuevos_datos["Placas"],
                        nuevos_datos["Modelo"], nuevos_datos["Marca"], nombre_combi))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Combi actualizada correctamente.")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EditarCombiApp(root)
    root.mainloop()
