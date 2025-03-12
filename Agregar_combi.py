import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, Canvas, filedialog
from PIL import Image, ImageTk
import sqlite3

def conectar_db():
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
    conn.close()

conectar_db()

def centrar_ventana(ventana, ancho=600, alto=400):  
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"+{x}+{y}")

class CombiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agrega tu combi")
        self.root.configure(bg="#2C2F33")

        # Marco principal
        self.frame = tk.Frame(root, padx=20, pady=20, bg="#2C2F33")
        self.frame.pack()

        # Botón de regreso
        self.btn_atras = tk.Button(self.frame, text="← Atrás", width=20, bg="#7289DA", fg="white",
                                   font=("Arial", 10, "bold"), command=self.root.destroy)
        self.btn_atras.grid(row=0, column=0, sticky='w', pady=5)

        # Título
        self.label_titulo = tk.Label(self.frame, text="Agrega tu combi", font=("Arial", 16, "bold"),
                                     fg="white", bg="#2C2F33")
        self.label_titulo.grid(row=0, column=1, columnspan=2)

        # Nombre de la combi (editable)
        self.combi_nombre = tk.StringVar(value="Combi 1")
        self.entry_combi_nombre = tk.Entry(self.frame, textvariable=self.combi_nombre, font=("Arial", 12), 
                                           width=22, bg="#99AAB5", fg="black")
        self.entry_combi_nombre.grid(row=1, column=0, columnspan=2, pady=5)
        create_tooltip(self.entry_combi_nombre, "Ejemplo: 'Combi 1', 'Unidad Azul'")

        # Sección de imagen (con botón para cargar)
        self.label_imagen = tk.Label(self.frame, text="[Imagen Combi Aquí]", width=20, height=5, 
                                     bg="#4F545C", fg="white")
        self.label_imagen.grid(row=2, column=0, columnspan=2, pady=10)

        self.btn_cargar_imagen = tk.Button(self.frame, text="Cargar Imagen", command=self.cargar_imagen, 
                                           width=22, bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
        self.btn_cargar_imagen.grid(row=3, column=0, columnspan=2, pady=5)

        self.imagen_path = None  

        # Formularios de información
        self.entries = {}
        info_labels = {
            "Rutas": "Ejemplo: 'Centro - Plaza'",
            "Horarios": "Ejemplo: '08:00AM, 18:00PM'",
            "Placas": "Ejemplo: 'ABC-1234'",
            "Modelo": "Ejemplo: 'Sprinter 2020'",
            "Marca": "Ejemplo: 'Mercedes-Benz'"
        }

        for i, (label, tooltip_text) in enumerate(info_labels.items()):
            lbl = tk.Label(self.frame, text=label, width=20, fg="white", bg="#2C2F33")
            lbl.grid(row=4+i, column=0, pady=2)
            entry = tk.Entry(self.frame, width=22, bg="#99AAB5", fg="black")
            entry.grid(row=4+i, column=1, pady=2)
            self.entries[label] = entry
            create_tooltip(entry, tooltip_text)

        # Botón para agregar combi
        self.btn_agregar_combi = tk.Button(self.frame, text="Agregar combi", width=22, bg="#43B581", fg="white",
                                           font=("Arial", 10, "bold"), command=self.guardar_combi)
        self.btn_agregar_combi.grid(row=9, column=0, columnspan=2, pady=10)

        # Sección de asientos
        self.asientos_count = tk.IntVar(value=0)
        
        self.label_asientos_texto = tk.Label(self.frame, text="Asientos", font=("Arial", 12), fg="white", bg="#2C2F33")
        self.label_asientos_numero = tk.Label(self.frame, textvariable=self.asientos_count, font=("Arial", 12), fg="white", bg="#2C2F33")
        
        self.label_asientos_texto.grid(row=1, column=2, sticky="w")
        self.label_asientos_numero.grid(row=1, column=2, sticky="e")
        
        self.btn_agregar_asiento = tk.Button(self.frame, text="Agregar asientos", command=self.agregar_asientos, width=22,
                                             bg="#7289DA", fg="white", font=("Arial", 10, "bold"))
        self.btn_agregar_asiento.grid(row=2, column=2, pady=10)

        self.canvas = Canvas(self.frame, width=300, height=300, bg="#23272A", highlightthickness=0)
        self.canvas.grid(row=3, column=2, rowspan=6, padx=20, pady=10)
        
        self.asientos = []

        centrar_ventana(self.root)

    def cargar_imagen(self):
        path = filedialog.askopenfilename(title="Selecciona una imagen",
                                          filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if path:
            self.imagen_path = path
            imagen = Image.open(path)
            w, h = imagen.size
            max_width, max_height = 200, 100
            ratio = min(max_width / w, max_height / h)
            new_size = (int(w * ratio), int(h * ratio))
            imagen = imagen.resize(new_size, Image.Resampling.LANCZOS)
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.label_imagen.config(image=self.imagen_tk, text="", width=new_size[0], height=new_size[1])

    def agregar_asientos(self):
        num_asientos = simpledialog.askinteger("Agregar asientos", "¿Cuántos asientos desea agregar?", minvalue=1, maxvalue=20)
        if num_asientos:
            self.asientos.clear()
            self.canvas.delete("all")
            for i in range(num_asientos):
                x = 50 + (i % 4) * 50
                y = 50 + (i // 4) * 50
                asiento = self.canvas.create_rectangle(x, y, x+30, y+30, fill="#7289DA", outline="white")
                self.canvas.create_text(x+15, y+15, text=str(i+1), fill="white")
                self.asientos.append(asiento)
            self.asientos_count.set(num_asientos)
            messagebox.showinfo("Éxito", f"Se agregaron {num_asientos} asientos correctamente.")

    def guardar_combi(self):
        datos = {k: v.get() for k, v in self.entries.items()}
        nombre_combi = self.combi_nombre.get()
        num_asientos = self.asientos_count.get()
        imagen_path = self.imagen_path

        if not nombre_combi or not all(datos.values()) or num_asientos <= 0:
            messagebox.showerror("Error", "Completa todos los campos correctamente.")
            return

        resumen = f"Nombre: {nombre_combi}\n" + "\n".join([f"{k}: {v}" for k, v in datos.items()]) + f"\nAsientos: {num_asientos}"
        if not messagebox.askyesno("Confirmar", f"¿Guardar esta combi?\n{resumen}"):
            return
        
        conn = sqlite3.connect("combis.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO combis (nombre, rutas, horarios, placas, modelo, marca, asientos, imagen_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre_combi, datos["Rutas"], datos["Horarios"], datos["Placas"], datos["Modelo"], datos["Marca"], num_asientos, imagen_path))

        conn.commit()
        conn.close()
        
        messagebox.showinfo("Guardado", "Combi guardada correctamente.")
                            
# Función para crear tooltips
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.wm_overrideredirect(True)
    tooltip.config(background="#FFFFE0", relief="solid", borderwidth=1)

    label = tk.Label(tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1, padx=5, pady=3)
    label.pack()

    import tkinter as tk

def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()  # Esconder el tooltip inicialmente
    tooltip.wm_overrideredirect(True)  # Quitar los bordes de la ventana
    tooltip.config(background="#FFFFE0", relief="solid", borderwidth=1)

    label = tk.Label(tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1, padx=5, pady=3)
    label.pack()

    def show_tooltip(event):
        x = widget.winfo_rootx() + event.x + 10
        y = widget.winfo_rooty() + event.y + 10
        tooltip.wm_geometry(f"+{x}+{y}")  # Posicionar el tooltip cerca del widget
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CombiApp(root)
    root.mainloop()


