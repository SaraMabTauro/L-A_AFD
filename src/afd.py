import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import csv

def automata_validator(input_string):
    transitions = {
        1: {'<': 2},
        2: {'s': 3},
        3: {'p': 4},
        4: {'a': 5},
        5: {'n': 6},
        6: {' ': 7},
        7: {'d': 8},
        8: {'a': 9},
        9: {'t': 10},
        10: {'a': 11},
        11: {'-': 12},
        12: {'i': 13},
        13: {'d': 14},
        14: {'=': 15},
        15: {'"': 16},
        16: {char: 17 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        17: {char: 18 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        18: {char: 19 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        19: {char: 20 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        20: {char: 21 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        21: {char: 22 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        22: {char: 23 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        23: {'|': 16, '"': 24},
        24: {'>': 25},
        25: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
        26: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    }
    transitions[26].update({'<': 27})
    transitions.update({
        27: {'/': 28},
        28: {'s': 29},
        29: {'p': 30},
        30: {'a': 31},
        31: {'n': 32},
        32: {'>': 33},
        33: {':': 34, ' ': 1, '.': 35},
        34: {' ': 1},
        35: {}
    })

    state = 1
    current_value = ""
    captured_values = []
    positions = []  # Lista para almacenar las posiciones como fila y columna
    full_sentence = ""
    i = 0
    row, col = 1, 1  # Inicializar fila y columna

    while i < len(input_string):
        char = input_string[i]

        # Manejar saltos de línea para ajustar fila y columna
        if char == '\n':
            row += 1
            col = 1
            i += 1
            continue

        if char in transitions[state]:
            state = transitions[state][char]

            if state == 25:
                current_value = ""
                start_position = (row, col)  # Guardar la posición de inicio (fila, columna)

            if state in [26, 34]:
                current_value += char

            if state == 33:
                if char == ':':
                    full_sentence += current_value.strip() + ": "
                    current_value = ""
                elif char == '.':
                    full_sentence = full_sentence.strip() + "."
                    captured_values.append(full_sentence)
                    positions.append(start_position)  # Guardar la posición de inicio
                    full_sentence = ""
                else:
                    full_sentence += current_value.strip() + " "
                    current_value = ""
                state = 1

        elif char in [' ', '\n']:
            i += 1
            col += 1
            continue

        elif state == 35:
            if full_sentence.strip():
                captured_values.append(full_sentence.strip())
                positions.append(start_position)
            full_sentence = ""
            break

        else:
            state = 1

        col += 1
        i += 1

    if full_sentence.strip():
        captured_values.append(full_sentence.strip())
        positions.append(start_position)

    return True, captured_values, positions

def save_to_csv(captured_values, positions):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Valor capturado', 'Fila', 'Columna'])
            for value, pos in zip(captured_values, positions):
                writer.writerow([value, pos[0], pos[1]])
        messagebox.showinfo("Éxito", "Los resultados se guardaron correctamente en el archivo CSV.")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML & TXT Files", "*.html;*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                validate_content(content)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

def validate_content(content):
    is_valid, captured_values, positions = automata_validator(content)
    if captured_values:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Cadena válida. Valores capturados:\n\n")
        for value, pos in zip(captured_values, positions):
            formatted_value = value.replace('\n', '').strip()  # Eliminando saltos de línea adicionales y espacios
            result_text.insert(tk.END, f"{formatted_value} (Fila: {pos[0]}, Columna: {pos[1]})\n\n")
        
        # Guardar los resultados en CSV
        save_to_csv(captured_values, positions)
    else:
        messagebox.showerror("Error", "No se capturaron valores válidos.")

def validate_manual_input():
    input_content = manual_input.get(1.0, tk.END).strip()
    if input_content:
        validate_content(input_content)
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa algún contenido para validar.")

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
result_text = ScrolledText(root, wrap=tk.WORD, width=90, height=20)
result_text.pack(padx=10, pady=10)

#Boton para exportar resultado
load_button2 = tk.Button(root, text="Exportar CSV", command=load_file)
load_button2.pack(pady=40)

# Ejecutar la aplicación
root.mainloop()