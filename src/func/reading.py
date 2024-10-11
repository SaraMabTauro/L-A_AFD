import tkinter as tk
from tkinter import filedialog, Text
from bs4 import BeautifulSoup

# Función para leer el archivo HTML
def leer_archivo_html(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo_html:
        contenido = archivo_html.read()
    return contenido

# Función para cargar el archivo y mostrar el nombre
def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos HTML", "*.html")])
    if ruta_archivo:
        label_archivo.config(text=ruta_archivo.split('/')[-1])  # Mostrar solo el nombre del archivo
        global contenido_html
        contenido_html = leer_archivo_html(ruta_archivo)

# Función de la acción "Ejecutar" para validar y mostrar resultados
def ejecutar_accion():
    if contenido_html:
        soup = BeautifulSoup(contenido_html, 'html.parser')
        enlaces = soup.find_all('a')  # Encontrar todos los enlaces
        texto_resultado.delete(1.0, tk.END)  # Limpiar el área de texto
        texto_resultado.insert(tk.END, f"Se encontraron {len(enlaces)} enlaces en el HTML.\n")
        for enlace in enlaces:
            texto_resultado.insert(tk.END, f"Enlace: {enlace.get('href')}\n")
    else:
        texto_resultado.insert(tk.END, "No se ha cargado ningún archivo.\n")

# Crear la ventana principal
root = tk.Tk()
root.title("Validador de HTML con Autómata")

# Crear widgets
label_archivo = tk.Label(root, text="No se ha cargado ningún archivo")
boton_cargar = tk.Button(root, text="Cargar Archivo HTML", command=cargar_archivo)
boton_ejecutar = tk.Button(root, text="Ejecutar", command=ejecutar_accion)
texto_resultado = Text(root, height=10, width=50)

# Posicionar widgets en la ventana
label_archivo.pack(pady=10)
boton_cargar.pack(pady=5)
boton_ejecutar.pack(pady=5)
texto_resultado.pack(pady=10)

contenido_html = ""  # Variable para almacenar el contenido del archivo HTML cargado

# Iniciar el bucle principal de Tkinter
root.mainloop()

