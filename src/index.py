import re

# Definir las transiciones del autómata
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

    # Estado 16 a 23: 7 caracteres alfanuméricos o | como transición
    16: {char: 17 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    17: {char: 18 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    18: {char: 19 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    19: {char: 20 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    20: {char: 21 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    21: {char: 22 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    22: {char: 23 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789|'},
    23: {'"': 24},

    # Estado 24 al 26: Aceptar letras para la definición
    24: {'>': 25},
    25: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'},

    # Estado 26: Recoge y repite las letras hasta el cierre del span
    26: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'},
    26: {'<': 27},
    27: {'/': 28},
    28: {'s': 29},
    29: {'p': 30},
    30: {'a': 31},
    31: {'n': 32},
    32: {'>': 33},

    # Estado final: Puede terminar con un punto o volver a empezar
    33: {'.': 34, '<': 1},
    34: {}
}

# Estado de aceptación final
accept_state = 34

# Función que verifica si la cadena es aceptada por el autómata
def is_accepted(string):
    state = 1  # Estado inicial
    for char in string:
        if char in transitions[state]:
            state = transitions[state][char]
        else:
            return False  # Si no hay transición para el carácter actual, la cadena no es aceptada
    return state == accept_state


# Función para procesar un archivo HTML y extraer las definiciones
def extract_definitions_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Utilizamos expresiones regulares para extraer solo las etiquetas <span data-id="...">...</span>
    pattern = re.compile(r'<span data-id="[^"]+">([^<]+)</span>')
    matches = pattern.findall(html_content)

    if not matches:
        print("No se encontraron etiquetas <span> válidas en el archivo.")
        return

    # Validar cada <span> extraída por el autómata
    valid = True
    for match in matches:
        span_tag = f'<span>{match}</span>'
        if not is_accepted(span_tag):
            valid = False
            break

    if valid:
        # Unimos las definiciones encontradas en una sola cadena
        definition = ' '.join(matches)
        print(f"Definición extraída: {definition}")
    else:
        print("El archivo HTML no es válido según el autómata.")

# Probar con un archivo HTML
extract_definitions_from_html('/home/luis-david/Desktop/automatas/src/archivo.html')
