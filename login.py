import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import os

# centrar ventana
def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

conectar_db()

# Guardar usuario en la base de datos
def guardar_usuario(usuario, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", (usuario, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Validar usuario en la base de datos
def validar_usuario(usuario, password):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Función para borrar texto por defecto
def on_entry_click(event, entry, texto_default, ocultar=False):
    if entry.get() == texto_default:
        entry.delete(0, tk.END)
        if ocultar:
            entry.config(show="*")

# Función para restaurar texto por defecto
def on_focus_out(event, entry, texto_default, ocultar=False):
    if entry.get() == "":
        entry.insert(0, texto_default)
        if ocultar:
            entry.config(show="")

# Mostrar pantalla de registro
def mostrar_registro():
    login_frame.pack_forget()
    registro_frame.pack()

# Mostrar pantalla de login
def mostrar_login():
    registro_frame.pack_forget()
    login_frame.pack()

# Validar entrada
def validar_entrada(usuario, password):
    if not usuario or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return False
    return True

# Registrar usuario
def crear_cuenta():
    usuario = entry_usuario_reg.get().strip()
    password = entry_password_reg.get().strip()
    confirm_password = entry_confirmar_reg.get().strip()

    if not validar_entrada(usuario, password):
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Las contraseñas no coinciden")
        return

    if guardar_usuario(usuario, password):
        messagebox.showinfo("Éxito", "Cuenta creada con éxito")
        mostrar_login()
    else:
        messagebox.showerror("Error", "El usuario ya existe")

# Iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get().strip()
    password = entry_password.get().strip()

    if not validar_entrada(usuario, password):
        return

    if validar_usuario(usuario, password):
        messagebox.showinfo("Inicio de sesión", f"Bienvenido, {usuario}!")
        root.destroy()
        subprocess.run(["python", "main.py"])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Crear ventana
root = tk.Tk()
root.title("Login y Registro")
ancho_ventana = 600
alto_ventana = 700
centrar_ventana(root, ancho_ventana, alto_ventana)
root.resizable(False, False)

# --------- LOGIN FRAME ---------
login_frame = tk.Frame(root)
login_frame.pack(expand=True)

img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img.jpg")
img = Image.open(img_path).resize((170, 170))
img = ImageTk.PhotoImage(img)


# Entradas de usuario y contraseña
entry_usuario = tk.Entry(login_frame, width=30, justify="center")
entry_usuario.pack(pady=5)
entry_usuario.insert(0, "Usuario")
entry_usuario.bind("<FocusIn>", lambda event: on_entry_click(event, entry_usuario, "Usuario"))
entry_usuario.bind("<FocusOut>", lambda event: on_focus_out(event, entry_usuario, "Usuario"))

entry_password = tk.Entry(login_frame, width=30, justify="center")
entry_password.pack(pady=5)
entry_password.insert(0, "Contraseña")
entry_password.bind("<FocusIn>", lambda event: on_entry_click(event, entry_password, "Contraseña", ocultar=True))
entry_password.bind("<FocusOut>", lambda event: on_focus_out(event, entry_password, "Contraseña", ocultar=True))

# Botón de inicio de sesión
tk.Button(login_frame, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)

# Enlace a registro
tk.Label(login_frame, text="¿No tienes cuenta?").pack()
tk.Button(login_frame, text="Regístrate", fg="blue", bd=0, command=mostrar_registro).pack()

# --------- REGISTRO FRAME ---------
registro_frame = tk.Frame(root)

tk.Label(registro_frame, text="Registro", font=("Arial", 14)).pack(pady=10)

entry_usuario_reg = tk.Entry(registro_frame, width=30, justify="center")
entry_usuario_reg.pack(pady=5)
entry_usuario_reg.insert(0, "Usuario")
entry_usuario_reg.bind("<FocusIn>", lambda event: on_entry_click(event, entry_usuario_reg, "Usuario"))
entry_usuario_reg.bind("<FocusOut>", lambda event: on_focus_out(event, entry_usuario_reg, "Usuario"))

entry_password_reg = tk.Entry(registro_frame, width=30, justify="center")
entry_password_reg.pack(pady=5)
entry_password_reg.insert(0, "Contraseña")
entry_password_reg.bind("<FocusIn>", lambda event: on_entry_click(event, entry_password_reg, "Contraseña", ocultar=True))
entry_password_reg.bind("<FocusOut>", lambda event: on_focus_out(event, entry_password_reg, "Contraseña", ocultar=True))

entry_confirmar_reg = tk.Entry(registro_frame, width=30, justify="center")
entry_confirmar_reg.pack(pady=5)
entry_confirmar_reg.insert(0, "Confirmar Contraseña")
entry_confirmar_reg.bind("<FocusIn>", lambda event: on_entry_click(event, entry_confirmar_reg, "Confirmar Contraseña", ocultar=True))
entry_confirmar_reg.bind("<FocusOut>", lambda event: on_focus_out(event, entry_confirmar_reg, "Confirmar Contraseña", ocultar=True))

# Botones de registro
tk.Button(registro_frame, text="Crear Cuenta", command=crear_cuenta).pack(pady=10)
tk.Button(registro_frame, text="Volver", command=mostrar_login).pack()

# Mostrar pantalla de login al iniciar
root.mainloop()
