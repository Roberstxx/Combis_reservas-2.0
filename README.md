# 🚐 Reservas de Combis

Sistema de reservas de combis desarrollado en Python con **Tkinter** para la interfaz gráfica.

## 📌 Características
- Registro e inicio de sesión de usuarios.
- Gestión de combis (agregar, editar, visualizar).
- Configuración de rutas y costos de viaje.
- Catálogo de combis disponibles.
- Administración de usuarios.

---

## 🛠 Requerimientos

### 🔹 Instalación de Python
Antes de comenzar, asegúrate de tener **Python 3.x** instalado en tu sistema. Puedes descargarlo desde:
🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

Para verificar que está instalado, ejecuta en la terminal o CMD:
```sh
python --version
```

### 🔹 Instalación de Dependencias
Este proyecto usa algunas librerías externas, que pueden instalarse fácilmente con:
```sh
pip install -r requirements.txt
```
Si usas Linux y Tkinter no está instalado, instálalo con:
```sh
sudo apt install python3-tk
```

---

## 🚀 Cómo Ejecutar el Proyecto

1️⃣ **Clona el repositorio**
```sh
git clone https://github.com/Roberstxx/Reservas-de-Combis.git
cd Reservas-de-Combis
```

2️⃣ **Instala las dependencias**
```sh
pip install -r requirements.txt
```

3️⃣ **Ejecuta la aplicación**
```sh
python main.py
```

---

## 📂 Estructura del Proyecto
```
Reservas-de-Combis/
│── assets/                 # Carpeta con imágenes y otros recursos
│── main.py                 # Archivo principal del sistema
│── login.py                # Sistema de autenticación (Login y Registro)
│── Agregar_combi.py        # Gestión de combis
│── usuarios.txt            # Base de datos local de usuarios (generado automáticamente)
│── requirements.txt        # Lista de dependencias
│── README.md               # Documentación del proyecto
```

---

## 📝 Notas
- El archivo `usuarios.txt` se genera automáticamente al registrar usuarios.
- Si tienes problemas al ejecutar en Linux, asegúrate de instalar `tkinter` manualmente.

¡Disfruta usando el sistema de **Reservas de Combis**! 🚐🎟️

