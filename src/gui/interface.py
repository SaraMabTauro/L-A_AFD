import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from src.afd.afd import HtmlTagAFD
from src.utils.file_operations import load_file_content, save_results_to_csv

def validate_content(content, result_text):
    afd = HtmlTagAFD()
    is_valid, captured_values, positions = afd.validate_text(content)
    result_text.delete(1.0, tk.END)
    if is_valid:
        result_text.insert(tk.END, "Cadena válida. Valores capturados:\n\n")
        for value, pos in zip(captured_values, positions):
            result_text.insert(tk.END, f"{value} Fila: {pos[0]}, Columna: {pos[1]}\n")
    else:
        messagebox.showinfo("Resultado", "No se encontraron valores válidos.")
        result_text.insert(tk.END, "No se encontraron valores válidos.")

def validate_manual_input(manual_input, result_text):
    input_content = manual_input.get(1.0, tk.END).strip()
    if input_content:
        validate_content(input_content, result_text)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa algún contenido para validar.")

def create_interface():
    root = tk.Tk()
    root.title("Validador de Autómata con HTML")
    root.geometry("800x700")

    load_button = tk.Button(root, text="Cargar archivo HTML/TXT", command=lambda: load_file_content(validate_content, result_text))
    load_button.pack(pady=10)

    manual_input = ScrolledText(root, wrap=tk.WORD, width=90, height=10)
    manual_input.pack(padx=10, pady=10)
    manual_input.insert(tk.END, "Ingresa contenido HTML o texto aquí...")

    validate_button = tk.Button(root, text="Validar contenido ingresado", command=lambda: validate_manual_input(manual_input, result_text))
    validate_button.pack(pady=10)

    result_text = ScrolledText(root, wrap=tk.WORD, width=90, height=17)
    result_text.pack(padx=10, pady=10)

    save_button = tk.Button(root, text="Exportar resultados a CSV", command=lambda: save_results_to_csv(result_text))
    save_button.pack(pady=10)

    root.mainloop() 