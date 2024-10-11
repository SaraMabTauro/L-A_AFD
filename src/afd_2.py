import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import csv

class HtmlTagAFD:
    def __init__(self):

        self.final_state = 35

        # Transiciones del autómata
        self.transitions = {
            (1, '<'): 2,
            (2, 's'): 3,
            (3, 'p'): 4,
            (4, 'a'): 5,
            (5, 'n'): 6,
            (6, ' '): 7,
            (7, 'd'): 8,
            (8, 'a'): 9,
            (9, 't'): 10,
            (10, 'a'): 11,
            (11, '-'): 12,
            (12, 'i'): 13,
            (13, 'd'): 14,
            (14, '='): 15,
            (15, '"'): 16,
            (23, '|'): 16,
            (23, '"'): 24,
            (24, '>'): 25,
            (26, '<'): 27,
            (27, '/'): 28,
            (28, 's'): 29,
            (29, 'p'): 30,
            (30, 'a'): 31,
            (31, 'n'): 32,
            (32, '>'): 33,
            (33, ':'): 34,
            (33, ','): 34,
            (33, 'l'): 34,
            (33, 'o'): 34,
            (33, 'a'): 34,
            (34, ':'): 34,
            (34, ','): 34,
            (34, 'l'): 34,
            (34, 'o'): 34,
            (34, 'a'): 34,
            (33, ' '): 1,       
            (33, '\n'): 1,  
            (33, '\t'): 1,     
            (33, '.'): 35,      
            (34, ' '): 1,       
            (34, '\n'): 1,      
            (34, '\t'): 1,      
        }

        # Transiciones para caracteres alfanuméricos
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz0123456789':
            self.transitions[(16, char)] = 17
            self.transitions[(17, char)] = 18
            self.transitions[(18, char)] = 19
            self.transitions[(19, char)] = 20
            self.transitions[(20, char)] = 21
            self.transitions[(21, char)] = 22
            self.transitions[(22, char)] = 23

        # Transiciones para caracteres alfabéticos
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz':
            self.transitions[(25, char)] = 26
            self.transitions[(26, char)] = 26
        
        self.saved_state = {26, 34, 35}

    def validate_text(self, text):
        current_state = 1 
        definitions_found = []
        extracted_text = ""
        line, col = 1, 0  # Inicializamos fila y columna
        positions = []  # Guardaremos las posiciones encontradas
        
        for char in text:
            col += 1  # Aumentamos la columna por cada carácter procesado

            if char == '\n':
                line += 1  # Saltamos a la siguiente línea si encontramos un salto de línea
                col = 0  # Reiniciamos la columna en cada nueva línea

            transition = (current_state, char)
            if transition in self.transitions:
                current_state = self.transitions[transition]
                # Guarda solo el contenido de las etiquetas
                if current_state in self.saved_state:
                    extracted_text += char
                if current_state == 27:
                    extracted_text += ' '
                if current_state == 35:
                    extracted_text += ' '
                
            else:
                if char in [' ', '\n', '\t']:
                    current_state = 1
                else:
                    current_state = 1
                    extracted_text = ""

            if current_state == self.final_state:
                definitions_found.append(extracted_text)                
                positions.append((line, col))  # Guardamos la fila y columna actual
                extracted_text = ""
                current_state = 1  
                
        if definitions_found:
            return True, definitions_found, positions 
        return False, [], []


# Función para cargar archivo HTML o TXT
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML & TXT Files", "*.html;*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                validate_content(content)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

# Función para validar el contenido
def validate_content(content):
    afd = HtmlTagAFD()
    is_valid, captured_values, positions = afd.validate_text(content)
    
    # Mostrar resultados en el área de texto
    result_text.delete(1.0, tk.END)  # Limpiar el área de texto
    if is_valid:
        result_text.insert(tk.END, "Cadena válida. Valores capturados:\n\n")
        for value, pos in zip(captured_values, positions):
            result_text.insert(tk.END, f"{value} Fila: {pos[0]}, Columna: {pos[1]}\n")
    else:
        messagebox.showinfo("Resultado", "No se encontraron valores válidos.")
        result_text.insert(tk.END, "No se encontraron valores válidos.")

# Función para validar el contenido ingresado manualmente
def validate_manual_input():
    input_content = manual_input.get(1.0, tk.END).strip()
    if input_content:
        validate_content(input_content)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa algún contenido para validar.")

# Guardar los resultados en un archivo CSV
def save_to_csv():
    captured_values = result_text.get(1.0, tk.END).strip().splitlines()
    if captured_values:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Valor capturado', 'Fila', 'Columna'])  # Encabezado del CSV
                    for value in captured_values:
                        writer.writerow([value])
                messagebox.showinfo("Éxito", "Los resultados se guardaron correctamente en el archivo CSV.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    else:
        messagebox.showwarning("Advertencia", "No hay valores para guardar.")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Validador de Autómata con HTML")
root.geometry("800x700")

# Botón para cargar archivo HTML o TXT
load_button = tk.Button(root, text="Cargar archivo HTML/TXT", command=load_file)
load_button.pack(pady=10)

# Caja de texto para ingreso manual
manual_input = ScrolledText(root, wrap=tk.WORD, width=90, height=10)
manual_input.pack(padx=10, pady=10)
manual_input.insert(tk.END, "Ingresa contenido HTML o texto aquí...")

# Botón para validar el contenido manual
validate_button = tk.Button(root, text="Validar contenido ingresado", command=validate_manual_input)
validate_button.pack(pady=10)

# Área de texto para mostrar los resultados
result_text = ScrolledText(root, wrap=tk.WORD, width=90, height=17)
result_text.pack(padx=10, pady=10)

# Botón para exportar resultados a CSV
save_button = tk.Button(root, text="Exportar resultados a CSV", command=save_to_csv)
save_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
