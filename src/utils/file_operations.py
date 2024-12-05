import csv
from tkinter import filedialog, messagebox
import tkinter as tk

def load_file_content(validate_content, result_text):
    file_path = filedialog.askopenfilename(filetypes=[("HTML & TXT Files", "*.html;*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                validate_content(content, result_text)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

def save_results_to_csv(result_text):
    captured_values = result_text.get(1.0, tk.END).strip().splitlines()
    if captured_values:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Valor capturado', 'Fila', 'Columna'])
                    for value in captured_values:
                        writer.writerow([value])
                messagebox.showinfo("Éxito", "Los resultados se guardaron correctamente en el archivo CSV.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    else:
        messagebox.showwarning("Advertencia", "No hay valores para guardar.")