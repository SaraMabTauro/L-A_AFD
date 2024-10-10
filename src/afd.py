import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

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
    full_sentence = ""
    i = 0

    while i < len(input_string):
        char = input_string[i]

        if char in transitions[state]:
            state = transitions[state][char]

            if state == 25:
                current_value = ""

            if state in [26, 34]:
                current_value += char

            if state == 33:
                # Adjusting the colon placement and sentence construction
                if char == ':':
                    full_sentence += current_value.strip() + ": "
                    current_value = ""
                elif char == '.':
                    full_sentence = full_sentence.strip() + "."
                    captured_values.append(full_sentence)
                    full_sentence = ""
                else:
                    full_sentence += current_value.strip() + " "
                    current_value = ""
                state = 1

        elif char in [' ', '\n']:
            i += 1
            continue

        elif state == 35:
            if full_sentence.strip():
                captured_values.append(full_sentence.strip())
            full_sentence = ""
            break

        else:
            state = 1

        i += 1

    if full_sentence.strip():
        captured_values.append(full_sentence.strip())

    return True, captured_values

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
    is_valid, captured_values = automata_validator(content)
    if captured_values:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Cadena válida. Valores capturados:\n\n")
        for value in captured_values:
            formatted_value = value.replace('\n', '').strip()  # Eliminando saltos de línea adicionales y espacios
            result_text.insert(tk.END, formatted_value + '\n\n')
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
root.title("Validador de Autómata con HTML y TXT")
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

# Ejecutar la aplicación
root.mainloop()
